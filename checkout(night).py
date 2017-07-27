# -*- coding:utf8 -*-
import pymssql
import smtplib
from datetime import *
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders


def send_email(from_addr, to_addr, subject, password):
    # 连接数据库
    hostname = '192.168.8.200'
    user = 'apiread'
    sqlpassword = 'wind,1234'
    database = 'PortfolioData'
    conn = pymssql.connect(hostname, user, sqlpassword, database, charset='utf8')
    cursor = conn.cursor()
    sql1 = '''select * from AppLog where convert(date,logdate,20)=convert(date,getdate() ,20) and AppSource='ImportWind' and DATEPART(HH, LogDate) >= 20 order by LogDate'''
    sheetstring = '''<table width="500" border="2" bordercolor="red" cellspacing="2">
                    <tr>
                    <td><strong>日期</strong></td>
                    <td><strong>日志标题</strong></td>
                    <td><strong>日志内容</strong></td>
                    </tr>
                    '''
    cursor.execute(sql1)
    data1 = cursor.fetchall()
    cursor.close()
    onestring = ''
    if data1:
        for i in range(0, len(data1)):
            d = data1[i][1].strftime('%Y-%m-%d %H:%M:%S')
            onestring = onestring + '''<tr><td>''' + d + '''</td> <td>''' + data1[i][3] + '''</td> <td>''' + data1[i][4] + '''</td> </tr>'''
        onestring = onestring.encode('utf8')
        onestring = sheetstring + onestring + '''</table>'''
    else:
        onestring = '查询无结果，请检查任务执行情况，谢谢!'
    msg = MIMEText(onestring, 'html', 'utf-8')
    msg['From'] = u'<%s>' % from_addr
    msg['To'] = u'<%s>' % to_addr
    msg['Subject'] = subject
    try:
        smtp = smtplib.SMTP_SSL("smtp.163.com", 465)
        smtp.set_debuglevel(1)
        smtp.ehlo("smtp.163.com")
        smtp.login(from_addr, password)
        smtp.sendmail(from_addr, [to_addr], msg.as_string())
        return True
    except Exception, e:
        print str(e)[1]
        return False
if __name__ == "__main__":
    if send_email(u"palh8888@163.com", u"jyyouzi@163.com", u"Wind_Api晚间任务执行报告", u"wind1234"):
        print '邮件发送成功！'
    else:
        print '邮件发送失败，请检查程序，谢谢！'

