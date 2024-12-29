## Denoising Implicit Feedback for Recommendation Based on ReChorus Framework:

本项目基于 ReChorus 框架，旨在复现 Denoising Implicit Feedback for Recommendation 这篇论文的自适应去噪训练（ADT）策略。ReChorus 是一个开源的推荐系统框架，用于处理多种推荐算法的研究和复现工作。ADT策略旨在解决推荐系统中隐式反馈数据存在噪声的问题，通过动态修剪大损失交互，有效减少了隐式反馈中噪声的影响，提高了推荐系统的性能。
- **Flexible**: implement new readers or runners for different datasets and experimental settings, and each model can be assigned with specific helpers.

## Structure

Generally, ReChorus decomposes the whole process into three modules:

- `src/`: 包含模型实现代码
  - `MY_MODEL.py`: 基于NeuMF模型实现的基本模型
  - `RmyRunner.py`: 应用加权损失（Truncated Loss），并引入RECALL@k和NDCG@k评估模型
  - `TmyRunner.py`: 应用截断损失（Truncated Loss），并引入RECALL@k和NDCG@k评估模型
  - `testBaseRunner.py`: 引入RECALL@k和NDCG@k评估模型
- `data/`: 数据文件存放目录，文件太大无法上传
  - 1`Grocery_and_Gourmet_Food/`: amazon数据集
  - 2`MINDTOPK`: MIND_small数据集(large数据太庞大了，受限于设备)
  - 3`ML_1MTOPK`: MovieLens-1M数据集

- `README.md`: 项目说明文档
## Usage
运行下面的命令：
```
python main.py --model_name MY_MODEL --epoch 200 --early_stop 50 --metric Recall,NDCG --emb_size 64 --layers '[64,32]' --lr 5e-4 --l2 1e-7 --dropout 0.2 --dataset 'Grocery_and_Gourmet_Food'
```
- `--model_name`: 模型名字
- `--epoch`: 训练轮次
- `--early_stop`: 早停轮次
- `--metric`: 评价模型
- `--emb_size`: 批处理大小
- `--layers`: 隐藏层大小
- `--lr`: 学习率
- `--l2`: 优化器的权重衰减
- `--dataset`: 数据集名称
- 根据具体需要，也可以添加其它参数，若要使用加权损失或者截断损失请在MY_MODEL.py文件里修改runner，截断损失默认使用alpha值为0.05，max_threshold值为0.7；加权损失默认使用beta值为0.05。

## Result


| Data                     | Metric                | myModel+TLoss                           | myModel+RLoss              | NeuMF                                   | BPRMF              | DirectAU                               | 
|:-------------------------|:----------------------|-----------------------------------------|------------------------|-----------------------------------------|------------------------|----------------------------------------|
| Grocery_and_Gourmet_Food | RECALL@20</br>NDCG@20<br/>RECALL@50<br/>NDCG@50 | 0.5442</br>0.2824<br/>0.7513<br/>0.3232 | 0.5991</br>0.3301<br/>0.7959<br/>0.3689 | 0.5416</br>0.2850<br/>0.7476<br/>0.3256 | 0.5585</br>0.2985<br/>0.7698<br/>0.3401 | 0.6170</br>0.3417<br/>0.8203<br/>0.3819 |
| MINDTOPK               | RECALL@20</br>NDCG@20<br/>RECALL@50<br/>NDCG@50 | 0.2735</br>0.1183<br/>0.5843<br/>0.1790 |  0.2765</br>0.1247<br/>0.6324<br/>0.1947| 0.3069</br>0.1281<br/>0.5255<br/>0.1711 | 0.2873</br>0.1175<br/>0.5225<br/>0.1644| 0.3039</br>0.1327<br/>0.5108<br/>0.1737 | 
| ML_1MTOPK           | RECALL@20</br>NDCG@20<br/>RECALL@50<br/>NDCG@50 | 0.7443</br>0.3682<br/>0.9482<br/>0.4093 |  0.7491</br>0.3665<br/>0.9419<br/>0.4052 | 0.7540</br>0.3639<br/>0.9520<br/>0.4037 | 0.7359</br>0.3502<br/>0.9457<br/>0.3923| 0.7070</br>0.0924<br/>0.3377<br/>0.3821| 


