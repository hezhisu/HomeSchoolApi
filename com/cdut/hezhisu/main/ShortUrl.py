import hashlib
from pip._vendor.requests.packages.urllib3.connectionpool import xrange
from setuptools.compat import unicode

__author__ = 'hezhisu'

import hashlib
import re
def __original_shorturl(url):
  '''
  算法：
  ① 将长网址用md5算法生成32位签名串，分为4段,，每段8个字符；
  ② 对这4段循环处理，取每段的8个字符, 将他看成16进制字符串与0x3fffffff(30位1)的位与操作，超过30位的忽略处理；
  ③ 将每段得到的这30位又分成6段，每5位的数字作为字母表的索引取得特定字符，依次进行获得6位字符串；
  ④ 这样一个md5字符串可以获得4个6位串，取里面的任意一个就可作为这个长url的短url地址。
  （出现重复的几率大约是n/(32^6) 也就是n/1,073,741,824，其中n是数据库中记录的条数）
  '''
  base32 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
       'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
       'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
       'y', 'z',
       '0', '1', '2', '3', '4', '5'
  ]
  m = hashlib.md5()
  m.update(url.encode("utf-8"))
  hexStr = m.hexdigest()
  hexStrLen = len(hexStr)
  subHexLen = int(hexStrLen / 8)
  output = []
  for i in range(0,subHexLen):
    subHex = '0x'+hexStr[i*8:(i+1)*8]
    res = 0x3FFFFFFF & int(subHex,16)
    out = ''
    for j in range(6):
      val = 0x0000001F & res
      out += (base32[val])
      res = res >> 5
    output.append(out)
  return output
def shorturl(url):
  t_shorturl = __original_shorturl(url)
  result = t_shorturl[0]
  return result

