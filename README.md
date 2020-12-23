## 模型服务

必须将模型挂载或者拷贝在/models目录下
指定模型名称MODEL_NAME必须和onnx文件名称相同,携带后缀
须知：模型对应的inputs

### onnx模型
*tiny-yolov3-11.onnx*

- {"input_1": {"type":"image","shape":[1,3,224,224]},"image_shape": {"type":"common","shape":[1,2]}}
- {"input_1": {"data":"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1600234043942&di=6b7f4f7bf90d08d844f4764d0331b186&imgtype=0&src=http%3A%2F%2Finews.gtimg.com%2Fnewsapp_match%2F0%2F11307101015%2F0.jpg","type":"url"},"image_shape": {"data":[[1,2]],"type":"common"}}

*mobilenetv2-7.onnx*
- {"data": {"type":"image","shape":[1,3,224,224]}}
- {"data": {"data":"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1600234043942&di=6b7f4f7bf90d08d844f4764d0331b186&imgtype=0&src=http%3A%2F%2Finews.gtimg.com%2Fnewsapp_match%2F0%2F11307101015%2F0.jpg","type":"url"}}

### tensorflow模型

*saved_models*

- {"dense_6_input":{"type":"image","shape":[1,784],dtype:"float"}}
- {"dense_7":{"type":"common","shape":[1,10],dtype:"float"}}
- {"dense_6_input": {"data":"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1600234043942&di=6b7f4f7bf90d08d844f4764d0331b186&imgtype=0&src=http%3A%2F%2Finews.gtimg.com%2Fnewsapp_match%2F0%2F11307101015%2F0.jpg","type":"url"}}

### h5模型
*106save03.h5*
- {"dense_6_input":{"type":"image","shape":[1,784]}}
- {"dense_7":{"type":"image","shape":[1,10]}}
- {"dense_6_input": {"data":"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1600234043942&di=6b7f4f7bf90d08d844f4764d0331b186&imgtype=0&src=http%3A%2F%2Finews.gtimg.com%2Fnewsapp_match%2F0%2F11307101015%2F0.jpg","type":"url"}}




