import torch
import torch.nn as nn
from models.BaseModel import GeneralModel

# python main.py --model_name MY_MODEL --epoch 200 --early_stop 50 --metric Recall,NDCG --emb_size 64 --layers '[64,32]' --lr 5e-4 --l2 1e-7 --dropout 0.2 --dataset 'Grocery_and_Gourmet_Food'

# 截断损失函数

def truncated_loss(predictions, labels, loss_fn, dynamic_threshold):
    loss_values = loss_fn(predictions, labels)  # 逐元素损失值
    mask = loss_values < dynamic_threshold  # 筛选低于阈值的损失值
    pruned_loss = loss_values[mask]
    if pruned_loss.numel() > 0:
        return pruned_loss.mean()  # 返回有效损失的平均值
    # 返回与计算图连接的零损失
    return torch.tensor(0.0, device=predictions.device, requires_grad=True)


class MY_MODEL(GeneralModel):
    reader = 'BaseReader'
    
    # runner = 'BaseRunner'
    runner = 'testBaseRunner'
    # runner = 'RmyRunner'
    # runner = 'TmyRunner'

    extra_log_args = ['emb_size', 'layers']

    @staticmethod
    def parse_model_args(parser):
        parser.add_argument('--emb_size', type=int, default=64,
                            help='Size of embedding vectors.')
        parser.add_argument('--layers', type=str, default='[64]',
                            help="Size of each layer.")
        return GeneralModel.parse_model_args(parser)

    def __init__(self, args, corpus):
        super().__init__(args, corpus)
        self.emb_size = args.emb_size
        self.layers = eval(args.layers)
        self._define_params()
        self.apply(self.init_weights)

    def _define_params(self):
        # GMF 部分
        self.mf_u_embeddings = nn.Embedding(self.user_num, self.emb_size)
        self.mf_i_embeddings = nn.Embedding(self.item_num, self.emb_size)

        # MLP 部分
        self.mlp_u_embeddings = nn.Embedding(self.user_num, self.emb_size)
        self.mlp_i_embeddings = nn.Embedding(self.item_num, self.emb_size)

        self.mlp = nn.ModuleList([])
        pre_size = 2 * self.emb_size

        for i, layer_size in enumerate(self.layers):
            self.mlp.append(nn.Linear(pre_size, layer_size))
            pre_size = layer_size
        self.dropout_layer = nn.Dropout(p=self.dropout)
        self.prediction = nn.Linear(pre_size + self.emb_size, 1, bias=False)
        


    def forward(self, feed_dict):
        self.check_list = []
        u_ids = feed_dict['user_id']  # [batch_size]
        i_ids = feed_dict['item_id']  # [batch_size, -1]

        u_ids = u_ids.unsqueeze(-1).repeat((1, i_ids.shape[1]))  # [batch_size, -1]

        mf_u_vectors = self.mf_u_embeddings(u_ids)
        mf_i_vectors = self.mf_i_embeddings(i_ids)
        mlp_u_vectors = self.mlp_u_embeddings(u_ids)
        mlp_i_vectors = self.mlp_i_embeddings(i_ids)

        mf_vector = mf_u_vectors * mf_i_vectors
        mlp_vector = torch.cat([mlp_u_vectors, mlp_i_vectors], dim=-1)
        for layer in self.mlp:
            mlp_vector = layer(mlp_vector).relu()
            mlp_vector = self.dropout_layer(mlp_vector)

        output_vector = torch.cat([mf_vector, mlp_vector], dim=-1)
        prediction = self.prediction(output_vector)
        return {'prediction': prediction.view(feed_dict['batch_size'], -1)}
    
    # def loss(self, out_dict: dict) -> torch.Tensor:
    #     # 在这里修改损失函数的计算逻辑
    #     predictions = out_dict['prediction']
    #     # 示例：使用均方误差作为新的损失函数
    #     loss = torch.nn.functional.mse_loss(predictions, torch.zeros_like(predictions))
    #     return loss