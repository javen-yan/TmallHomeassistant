#coding: utf-8
import os 
import sys
import time

base = os.path.dirname(os.path.abspath(__file__))
api_file_path = os.path.join(base, 'oauth_page', 'src','api.js')
api_setting_path = os.path.join(base, 'OauthDjango', 'OauthDjango','settings.py')

def modify_page_url():
    hole_lines = None
    with open(api_file_path, 'r',encoding='utf-8') as api:
        hole_lines = api.readlines()
    need_modify_url = hole_lines[3]
    input_url = input('请输入您的API请求地址:')
    print('您输入的地址为: %s' % input_url)
    stable_url ='''  _base_url = '%s'\n''' % input_url
    hole_lines[3] = stable_url
    print('正在修改请求地址')
    with open(api_file_path, 'w') as api_write:
        api_write.writelines(hole_lines)
    time.sleep(1)
    print('请求地址修改完成')


def modify_api_setting():
    hole_lines = None
    with open(api_setting_path, 'r',encoding='utf-8') as api_settings:
        hole_lines = api_settings.readlines()

    HOST = input('请输入您的服务器域名或者IP:')
    stable_HOST = '''HOST = '%s'\n''' %  HOST
    hole_lines[10] = stable_HOST
    print(hole_lines[10])

    DB = input('请输入您的数据库NAME:')
    DB_USER = input('请输入您的数据库user:')
    DB_PW = input('请输入您的数据库password:')
    DB_HOST = input('请输入您的数据库HOST:')
    DB_PORT = input('请输入您的数据库PORT:')

    DB_NAME = "        'NAME': '%s',\n" % DB
    USER = "        'USER': '%s',\n" % DB_USER
    PASSWORD = "        'PASSWORD': '%s',\n" % DB_PW
    HOSTS = "        'HOST': '%s',\n" % DB_HOST
    PORT = "        'PORT': '%s',\n" % DB_PORT
    
    hole_lines[61] = DB_NAME
    hole_lines[62] = USER
    hole_lines[63] = PASSWORD
    hole_lines[64] = HOSTS
    hole_lines[65] = PORT

    print('正在修改配置文件')
    with open(api_setting_path, 'w') as api_write:
        api_write.writelines(hole_lines)
    time.sleep(1)
    print('配置文件修改完成')

def build_page():
    os.chdir(os.path.dirname(os.path.dirname(api_file_path)))
    has_install_npm = input('是否已经安装好npm相关环境 Y/N:')
    if has_install_npm == 'Y' or has_install_npm == 'y':
        print('正在获取项目依赖')
        os.system('npm install')
        print('正在编译前端页面')
        os.system('npm run build')
        print('正在压缩文件')
        os.system('zip -q -r dist.zip ./dist')
        print('请将dist.zip上传到服务器')
    elif has_install_npm == 'N' or has_install_npm == 'n':
        print('请先安装好 NPM 环境')
    else: 
        return



def main():
    print('第一步: 修改前端请求地址')
    modify_page_url()
    print('第一步 已完成')   
    print('第二步: 修改后端配置文件')
    modify_api_setting()
    print('第二步 已完成') 
    print('第三步: 编译前端页面')
    build_page()
    print('第三步 已完成') 


if __name__ == "__main__":
    main()