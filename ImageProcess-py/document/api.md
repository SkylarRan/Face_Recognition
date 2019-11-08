# 图形处理API接口文档
        服务器: http://localhost:5000
        数据库: mysql
***
# 历史记录

日期|版本|更新内容
--|--|--
191108|1.0.1|增加API， blacklist, recognize

***
# 接口规范

## Request Header
    请求头域内容
> 
#### Host: `http://host:port/app/v1.0`
#### Content-Type: `application/json`

## Response Header
    响应头域内容
> 

***
# 服务器测试

## 测试
> 
#### HttpMethod `GET`
#### Url: `/test`
#### Request: 
param       |type       |nullable   |description
------------|-----------|-----------|-----------
Null

#### Response:
param|type|description
-|-|-
status|bool|是否成功

***
# 黑名单
    
## 查询
>
#### HttpMethod `GET`
#### Url: `/blacklists?offset=0&limit=10`
#### Request: 
param       |type       |nullable   |description
------------|-----------|-----------|-----------
offset      |int        |false      |偏移数 
limit       |int        |false      |限制数

#### Response:
param|type|description
-|-|-
status|bool|是否成功
total|int|黑名单总条数
data|array|数据
data.id|string| uuid
data.image|string|图像相对路径
data.name|string|姓名
data.memo|string|备注

#### Sample
```
response:
{
    "status": true,  
    "data": [
        {
        "id": "ba408522-fbc9-11e9-aeba-38d547e24f4d",
        "image": "blacklist/ba405e28-fbc9-11e9-aed6-38d547e24f4d.jpg",
        "memo": "yellow",
        "name": "fei"
        }
    ],
    "total": 6
}
```

## 新增/修改
>
#### HttpMethod `POST`
#### Url: `/blacklist/save`
#### Request: 
param       |type       |nullable   |description
------------|-----------|-----------|-----------
id      |string        |新增true， 修改false| 黑名单id 
name    |string        |新增false      | 姓名
image   |string        |新增false      | 图片相对路径
memo    |string        |true           | 备注 

#### Response:
param|type|description
-|-|-
status|bool|是否成功

#### Sample
```
response:
{
    "status": true 
}
```

## 删除
>
#### HttpMethod `POST`
#### Url: `/blacklist/delete`
#### Request: 
param       |type       |nullable   |description
------------|-----------|-----------|-----------
id      |string        |false| 黑名单id 

#### Response:
param|type|description
-|-|-
status|bool|是否成功

#### Sample
```
response:
{
    "status": true 
}
```


***
# 识别
    
## 开始识别
>
#### HttpMethod `POST`
#### Url: `/recognize/start`
#### Request: 
param       |type       |nullable   |description
------------|-----------|-----------|-----------
rtmp        |string     | false     |rtmp流地址 
name        |string     | false     |camera名称
location    |string     | false     |位置

#### Response:
param|type|description
-|-|-
status|bool|是否成功
data| array|识别线程id数组

#### Sample
```
response:
{
  "data": [
    10248
  ],
  "status": true
}
```

## 停止识别
>
#### HttpMethod `POST`
#### Url: `/recognize/stop`
#### Request: 
param       |type       |nullable   |description
------------|-----------|-----------|-----------
tids        |array      | array     |识别线程id

#### Response:
param|type|description
-|-|-
status|bool|是否成功

#### Sample
```
response:
{
  "status": true
}
```


