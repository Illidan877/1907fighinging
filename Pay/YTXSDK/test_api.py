from CCPRestSDK import REST
import configparser

#主账号
accountSid = 'x'

#主账号Token
accountToken = 'x'

#应用Id
appId ='x'

#请求地址，格式如下，不需要http://
serverIP = 'app.cloopen.com'

#端口
serverPort='8883'

#REST版本号
softVersion='2013-12-26'

  # 发送短信
  # @param to 手机号
  # @param datas 数据内容  格式为数组如{'12','34'} 不需要用''替换
  # @param $tempId 模板Id

def send_template_SMS(to,datas,tempId):
    
    #初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    return rest.sendTemplateSMS(to,datas,tempId)