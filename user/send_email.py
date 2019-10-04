import smtplib
from company.celeryconfig import app


@app.task(queue='Email')
def send_email(EmailMultiAlternatives, from_emial, to_email, subject, message, html_content, verification_code, cache):
    """

    :param EmailMultiAlternatives: 发送邮件实例
    :param from_emial: 源邮箱地址
    :param to_email: 目标地址
    :param subject: 主题
    :param message: 内容
    :param html_content:html内容
    :param verification_code: 验证码
    :param cache: redis缓存实例
    :return:
    """
    msg = EmailMultiAlternatives(subject, message, from_emial, [to_email])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
        cache.set(to_email, verification_code)
    except smtplib.SMTPDataError as e:
        print(e)
