# 购物车模块-接口说明

## 一、购物车模块概述：	

​	购物车模块主要提供用户本产品的基础。购物车模块提供一下功能：

>添加购物车
>
>查询购物车
>
>删除购物车
>
>购物车商品数量添加/减少
>
>购物车商品单选/取消单选
>
>购物车商品全选/取消全选
>
>合并购物车

## 二、事件定义

### 添加购物车

​		用户未登陆状态下进入商品详情页，选择规格和数量，将商品加入到购物车，数据将保存到前端的浏览器的本地存储里。

​		用户登陆状态下进入商品详情页，选择规格和数量，将商品加入到购物车，前端会通过ajax进行与后端交互。

### 查询购物车

​		用户未登录状态下进入购物车页面，前端通过浏览器的本地存储保存的数据展示给用户。

​		用户登录状态下进入购物车页面，后端通过redis存好的商品数据，传给前端展示给用户。

### 删除购物车

​		用户进入购物车页面，点击购物车某个商品删除按钮，会有一个弹框显示确定删除和不删除，点击确定删除按钮，商品会被删除。

### 购物车商品

​		商品数量增加和减少： 用户进入购物车页面，点击商品 “+” 按钮，将商品数量增加1个。点击商品 “-” 按钮，将商品数量减少1个。

​		商品单选和取消单选：用户进入购物车页面，默认进入购物车页面单选是 ”√“ ，取消单件商品点击单选按钮，按钮显示空，选择单件商品点击单选按钮，按钮显示 ”√“。

​		商品全选和取消全选：用户进入购物车页面，默认进入购物车页面全选是 ”√“ ，取消全部商品点击全选按钮，按钮显示空，选择全部商品点击全选按钮，按钮显示 ”√“。

### 合并购物车

​		用户在登陆时，创建token，会将用户未登陆状态下浏览器本地存储的购物车商品数据传给后端，后端通过redis存储的商品数量，做数量比较将商品数量最多的存入redis，返还给前端显示。 

## 三、API接口说明

### 1.添加购物车

在登陆的状态下添加购物车

#### 事件触发：

页面名：**product_details.html**

![1574767684004](images/1574767684004.png)

#### 触发结果：

​	触发成功：

![1574767923411](images/1574767923411.png)

![1574768001137](images/1574768001137.png)

​	触发失败：

![](images\微信截图_20191127172456.png)

![1574768258153](images/1574768258153.png)



**URL**： ``127.0.0.1:8000/v1/carts/<username> ``

**请求方式**：POST

**请求参数**：JSON

|  参数  | 类型 | 是否必须 |    说明    |
| :----: | :--: | :------: | :--------: |
| sku_id | int  |    是    | 商品sku_id |
| count  | int  |    是    |    数量    |

```
请求示例：
{ "sku_id":2,"count":"1"}
```

**返回值**：JSON

**响应格式**：

```
# 正确响应：
{"code":200,"data":skus_list}

# 错误响应：
{"code":xxx,"error":xxx}
```

| 字段  |   含义   | 类型 | 备注                        |
| :---: | :------: | :--: | --------------------------- |
| code  |  状态码  | int  | 默认正常为200，异常见状态码 |
| data  | 具体数据 | dict | 与error二选一               |
| error | 错误信息 | char | 与data二选一                |

skus_list参数信息

| 参数               | 类型    | 是否必须 | 说明                            |
| ------------------ | ------- | -------- | ------------------------------- |
| id                 | int     | 是       | 商品sku_id                      |
| name               | str     | 是       | 商品名称                        |
| count              | int     | 是       | 商品数量                        |
| default_image_url  | str     | 是       | 商品默认图片路径                |
| price              | decimal | 是       | 商品单价                        |
| sku_sale_attr_name | list    | 是       | 商品属性                        |
| sku_sale_attr_val  | list    | 是       | 商品属性值                      |
| selected           | int     | 是       | 商品的选中状态（0未选中,1选中） |

```json
#sku_list中数据示例 
[{		
  'id': 1, 
  'name': '安踏a 大尺寸灰色',
  'count': 9, 
  'selected': 1, 
  'default_image_url': '2_SYDQN2A.jpg', 
  'price': Decimal('123.00'), 
  'sku_sale_attr_name': ['安踏a/颜色', '安踏a/尺寸'], 
  'sku_sale_attr_val': ['灰色', '18寸']
}
```

状态码参数：

| 状态码 | 响应信息         | 原因短句                    |
| ------ | ---------------- | --------------------------- |
| 200    | 正常             | OK                          |
| 30101  | 未找到商品       | SKU query error             |
| 30102  | 传参不正确       | Incorrect pass of reference |
| 30103  | 购买数量超过库存 | exceeds the inventory       |
| 30104  | 未找到用户       | User query error            |

#### 后端代码:

```python
redis_conn = get_redis_connection('cart')
class CartVIew(View):    
    def dispatch(self, request, *args, **kwargs):
        # 实现对于请求方法的封装   
    
    def get_car_list(self,user_id):
        # 对于购物车中数据的结构化
    
    @logging_check
    def post(self, request, username):
      	"""
      	1.获取用户传递数据。包括前端传递的数据。sku ID\ count
      	2.判断购买数量和库存类比。
      	3.判断用户是否合法
      	4.实现购物车的增加：
      		4.1 如果购物车服务器缓存中已经有，那么累加，存入缓存
      		4.2 如果购物车的服务器缓存中没有，那么新增。存入缓存
      	5.获取当前登陆用户购物车中的商品，返回前端。
      	"""
```



### 2.查询购物车

#### 事件触发:

页面名：**index.html**

页面名：**cart.html** 

![1574782690588](images/1574782690588.png)

#### 触发结果:

![1574782806563](images/1574782806563.png)

**URL**： 127.0.0.1:8000/v1/carts/<username>

**请求方式**: GET

**请求参数**：无

**返回值**：JSON

**响应格式**：

```
# 正常响应： 
{"code":200,"data":skus_list}

# 异常响应
{"code":xxx,"error"：xxxx}
```

| 字段  | 含义     | 类型 | 备注                        |
| ----- | -------- | ---- | --------------------------- |
| code  | 状态码   | int  | 默认正常为200，异常见状态码 |
| data  | 具体数据 | dict | 与error二选一               |
| error | 错误信息 | char | 与data二选一                |

sku_list参数信息

| 参数               | 类型    | 是否必须 | 说明                             |
| ------------------ | ------- | -------- | -------------------------------- |
| id                 | int     | 是       | 商品sku_id                       |
| name               | str     | 是       | 商品名称                         |
| count              | int     | 是       | 商品数量                         |
| default_image_url  | str     | 是       | 商品默认图片路径                 |
| price              | decimal | 是       | 商品单价                         |
| sku_sale_attr_name | list    | 是       | 商品属性                         |
| sku_sale_attr_val  | list    | 是       | 商品属性值                       |
| selected           | int     | 是       | 商品的选中状态（0未选中，1选中） |

```json
#sku_list中数据示例 
[{		
  'id': 1, 
  'name': '安踏a 大尺寸灰色',
  'count': 9, 
  'selected': 1, 
  'default_image_url': '2_SYDQN2A.jpg', 
  'price': Decimal('123.00'), 
  'sku_sale_attr_name': ['安踏a/颜色', '安踏a/尺寸'], 
  'sku_sale_attr_val': ['灰色', '18寸']
}]
```

状态码参数

| 状态码 | 响应信息   | 原因短语         |
| ------ | ---------- | ---------------- |
| 200    | 正常       | OK               |
| 30104  | 未找到用户 | User query error |

#### 后端代码:

```python
redis_conn = get_redis_connection('cart')
class CartVIew(View):
    @logging_check
    def get(self, request, username):
       """
       1.判断是否为当前的正常登陆用户。
       2.获取当前用户在redis数据库中的缓存。
       3.返回给前端。
       """

```



### 3.删除购物车数据

#### 事件触发:

页面名：**cart.html** 

![1574783291641](images/1574783291641.png)

#### 触发结果:

![1574783416421](images/1574783416421.png)

![1574783443996](images/1574783443996.png)



**URL**： 127.0.0.1:8000/v1/carts/<username> 

**请求方式**：DELETE

**请求参数**

```python
#请求参数示例： 
{"sku_id":1001}
```

| 参数   | 类型 | 是否必须 | 说明       |
| ------ | ---- | -------- | ---------- |
| sku_id | int  | 是       | 商品sku_id |

**返回值**：json

**响应格式**：

```python
# 正常响应： 
{"code":200,"data":skus_list}

# 异常响应
{"code":xxx,"error"：xxxx}
```

| 字段  | 含义     | 类型 | 备注                            |
| ----- | -------- | ---- | ------------------------------- |
| code  | 状态码   | int  | 默认正常为200，异常见状态码参考 |
| data  | 具体数据 | dict | 与error二选一                   |
| error | 错误信息 | char | 与data二选一                    |

skus_list参数信息

| 参数               | 类型    | 是否必须 | 说明                             |
| ------------------ | ------- | -------- | -------------------------------- |
| id                 | int     | 是       | 商品sku_id                       |
| name               | str     | 是       | 商品名称                         |
| count              | int     | 是       | 商品数量                         |
| default_image_url  | str     | 是       | 商品默认图片路径                 |
| price              | decimal | 是       | 商品单价                         |
| sku_sale_attr_name | list    | 是       | 商品属性                         |
| sku_sale_attr_val  | list    | 是       | 商品属性值                       |
| selected           | int     | 是       | 商品的选中状态（0未选中，1选中） |

```python
#sku_list中数据示例 
[{		
  'id': 1, 
  'name': '安踏a 大尺寸灰色',
  'count': 9, 
  'selected': 1, 
  'default_image_url': '2_SYDQN2A.jpg', 
  'price': Decimal('123.00'), 
  'sku_sale_attr_name': ['安踏a/颜色', '安踏a/尺寸'], 
  'sku_sale_attr_val': ['灰色', '18寸']
}]
```

状态码参考

| 状态码 | 响应信息   | 原因短句         |
| ------ | ---------- | ---------------- |
| 200    | 正常       | OK               |
| 30101  | 未找到商品 | SKU query error  |
| 30104  | 未找到用户 | User query error |

#### 后端代码

```python
class CartVIew(View):
    
    @logging_check
    def delete(self, request, username):
        """
        1.拿出用户需要删除的sku_id 
        2.删除用户的数据库中的sku_id
        3.返回购物车中的数据。
        """
        pass
```



### 4.购物车页面商品数量增加减

#### 事件触发:

页面名：**cart.html** 

![1574783885360](images/1574783885360.png)

#### 触发结果:

![1574783996491](images/1574783996491.png)

**URL**： 127.0.0.1:8000/v1/carts/<username> 

**请求方式**：PUT

**请求参数**：JSON

| 参数   | 类型 | 是否必须 | 说明           |
| ------ | ---- | -------- | -------------- |
| sku_id | int  | 是       | 商品sku_id     |
| count  | int  | 是       | 前端显示的数量 |
| state  | str  | 是       | 判断事件状态   |

```python
#请求示例 add
{'sku_id':1001,count:1,state:'add'}
#请求示例 del
{'sku_id':1001,count:1,state:'del'}
```

**返回值**：JSON

**响应格式**：

```python
# 正常响应： 
{"code":200,"data":skus_list}

# 异常响应
{"code":xxx,"error"：xxxx}
```

| 字段  | 含义     | 类型 | 备注                        |
| ----- | -------- | ---- | --------------------------- |
| code  | 状态码   | int  | 默认正常为200，异常见状态码 |
| data  | 具体数据 | dict | 与error二选一               |
| error | 错误信息 | char | 与data二选一                |

skus_list参数信息

| 参数               | 类型    | 是否必须 | 说明                             |
| ------------------ | ------- | -------- | -------------------------------- |
| id                 | int     | 是       | 商品sku_id                       |
| name               | str     | 是       | 商品名称                         |
| count              | int     | 是       | 商品数量                         |
| default_image_url  | str     | 是       | 商品默认图片路径                 |
| price              | decimal | 是       | 商品单价                         |
| sku_sale_attr_name | list    | 是       | 商品属性                         |
| sku_sale_attr_val  | list    | 是       | 商品属性值                       |
| selected           | int     | 是       | 商品的选中状态（0未选中，1选中） |

```python
#sku_list中数据示例 
[{		
  'id': 1, 
  'name': '安踏a 大尺寸灰色',
  'count': 9, 
  'selected': 1, 
  'default_image_url': '2_SYDQN2A.jpg', 
  'price': Decimal('123.00'), 
  'sku_sale_attr_name': ['安踏a/颜色', '安踏a/尺寸'], 
  'sku_sale_attr_val': ['灰色', '18寸']
}]
```

状态码参考

| 状态码 | 响应信息   | 原因短语         |
| ------ | ---------- | ---------------- |
| 200    | 正常       | OK               |
| 30101  | 未找到商品 | SKU query error  |
| 30104  | 未找到用户 | User query error |

#### 后端代码

```python
redis_conn = get_redis_connection('cart')

class CartVIew(View):
    @logging_check
    def put(self, request, username):
        """
        1.取出前端传递的数据。
        2.根据前端传递的标志进行判断是增加、减少
        	2.1 如果是增加的话，对于数量增加。
        	2.2 如果是删除的话，对于数量减少。
        """
```

### 5.购物车商品单选和取消单选

#### 事件触发

页面名：**cart.html** 

![1574818291352](images/1574818291352.png)

#### 触发结果

![1574818354438](images/1574818354438.png)

**URL**： 127.0.0.1:8000/v1/carts/<username>

**请求方式:** PUT

**请求参数**：JSON

| 参数   | 类型 | 是否必须 | 说明                   |
| ------ | ---- | -------- | ---------------------- |
| sku_id | int  | 是       | 购物车显示商品的sku_id |
| state  | str  | 是       | 判断事件状态           |

```python
#请求示例 select  
{'sku_id':1001,state:'select'}
#请求示例 unselect 
{'sku_id':1001,state:'unselect'}
```

**返回值**：JSON

**响应格式**

```python
# 正常响应： 
{"code":200,"data":skus_list}

# 异常响应
{"code":xxx,"error"：xxxx}
```

| 字段  | 含义     | 类型 | 备注                            |
| ----- | -------- | ---- | ------------------------------- |
| code  | 状态码   | int  | 默认正常为200，异常见状态码参考 |
| data  | 具体数据 | dict | 与error二选一                   |
| error | 错误信息 | char | 与data二选一                    |

skus_list参数信息

| 参数               | 类型    | 是否必须 | 说明                             |
| ------------------ | ------- | -------- | -------------------------------- |
| id                 | int     | 是       | 商品sku_id                       |
| name               | str     | 是       | 商品名称                         |
| count              | int     | 是       | 商品数量                         |
| default_image_url  | str     | 是       | 商品默认图片路径                 |
| price              | decimal | 是       | 商品单价                         |
| sku_sale_attr_name | list    | 是       | 商品属性                         |
| sku_sale_attr_val  | list    | 是       | 商品属性值                       |
| selected           | int     | 是       | 商品的选中状态（0未选中，1选中） |

```python
#sku_list中数据示例 
[{		
  'id': 1, 
  'name': '安踏a 大尺寸灰色',
  'count': 9, 
  'selected': 1, 
  'default_image_url': '2_SYDQN2A.jpg', 
  'price': Decimal('123.00'), 
  'sku_sale_attr_name': ['安踏a/颜色', '安踏a/尺寸'], 
  'sku_sale_attr_val': ['灰色', '18寸']
}]
```

状态码参考

| 状态码 | 响应信息   | 原因短语         |
| ------ | ---------- | ---------------- |
| 200    | 正常       | OK               |
| 30101  | 未找到商品 | SKU query error  |
| 30104  | 未找到用户 | User query error |

#### 后端代码

```python
redis_conn = get_redis_connection('cart')

class CartVIew(View):
    @logging_check
    def put(self, request, username):
        """
        1.获取前端传递的数据。
        2.根据前端传递数据取出取消勾选的skuid。
        3.修改redis中的数据。
        4.返回响应的购物车数据。
        """
    		pass
```

### 6.购物车商品全选/取消全选

#### 事件触发

页面名：**cart.html** 

![1574818659463](images/1574818659463.png)

#### 触发结果

![1574818713029](images/1574818713029.png)

**URL**： 127.0.0.1:8000/v1/carts/<username>

**请求方式:** PUT

**请求参数**：JSON

| 参数  | 类型 | 是否必须 | 说明         |
| ----- | ---- | -------- | ------------ |
| state | str  | 是       | 判断事件状态 |

```json
# 全选请求示例： 
{state:'selectall'}
# 取消请求示例 
{state:'unselectall'}
```

**返回值**：JSON

**响应格式**

```python
# 正常响应： 
{"code":200,"data":skus_list}

# 异常响应
{"code":xxx,"error"：xxxx}
```

| 参数               | 类型    | 是否必须 | 说明                             |
| ------------------ | ------- | -------- | -------------------------------- |
| id                 | int     | 是       | 商品sku_id                       |
| name               | str     | 是       | 商品名称                         |
| count              | int     | 是       | 商品数量                         |
| default_image_url  | str     | 是       | 商品默认图片路径                 |
| price              | decimal | 是       | 商品单价                         |
| sku_sale_attr_name | list    | 是       | 商品属性                         |
| sku_sale_attr_val  | list    | 是       | 商品属性值                       |
| selected           | int     | 是       | 商品的选中状态（0未选中，1选中） |

```python
#sku_list中数据示例 
[{		
  'id': 1, 
  'name': '安踏a 大尺寸灰色',
  'count': 9, 
  'selected': 1, 
  'default_image_url': '2_SYDQN2A.jpg', 
  'price': Decimal('123.00'), 
  'sku_sale_attr_name': ['安踏a/颜色', '安踏a/尺寸'], 
  'sku_sale_attr_val': ['灰色', '18寸']
}]
```

状态码参考

| 状态码 | 响应信息   | 原因短句         |
| ------ | ---------- | ---------------- |
| 200    | 正常       | OK               |
| 30104  | 未找到用户 | User query error |

#### 后端代码

```python
redis_conn = get_redis_connection('cart')

class CartVIew(View):
    @logging_check
    def put(self, request, username):
        """
        1.判断传递的数据state的值。
        2.根据state的值进行匹配操作。
        3.对该用户所有的购物车数据进行操作。
        """
        pass
```

### 7.合并购物车

登陆模块会调用合并购物车函数

#### 触发事件

页面名：**cart.html** 

![1574826020270](images/1574826020270.png)

![1574826104974](images/1574826104974.png)

#### 触发结果

![1574826198391](images/1574826198391.png)

**请求参数**：JSON

| 参数   | 类型 | 是否必须 | 说明     |
| ------ | ---- | -------- | -------- |
| sku_id | str  | 是       | 商品id   |
| count  | int  | 是       | 商品数量 |

**响应格式**：

```json
{ 
  'code': 200,
  'username': user.username,
  'token': token.decode(),
  'len':cart_len}
}
```

| 字段     | 含义     | 类型 | 备注          |
| -------- | -------- | ---- | ------------- |
| code     | 状态码   | int  | 默认正常为200 |
| username | 用户名   | char | 必选          |
| data     | 具体数据 | dict | 必选          |

参数信息

| 参数     | 类型 | 是否必须 | 说明             |
| -------- | ---- | -------- | ---------------- |
| token    | char | 是       | token令牌        |
| len      | int  | 是       | 购物车里数据长度 |
| username | char | 是       | 用户名           |

状态码参考

| 状态码 | 响应信息 | 原因短语 |
| ------ | -------- | -------- |
| 200    | 正常     | OK       |

#### 后端代码

```python
def merge_cart(user,token,cart_data):
    #判断如果未登录购物车为空
    """
    1.如果用户登陆之后 ，购物车中为空，直接返回登陆的状态。
    2.如果用户登陆之后前端传递的购物车中的同一个商品数据，和redis中数据数量不一致。则选取最多的为准。
    3.如果不在购物车中，直接讲商品数据存到redis中。
    4.完成登陆。
    """
    pass
  
		    
```

