import os
import ssl
import whisper
import sys
import urllib3
import certifi
from tqdm import tqdm

def setup_proxy():
    """设置代理"""
    os.environ['https_proxy'] = 'http://127.0.0.1:8118'
    os.environ['http_proxy'] = 'http://127.0.0.1:8118'

def download_model(model_name):
    """
    下载指定的 Whisper 模型
    
    Args:
        model_name (str): 要下载的模型名称
    """
    print(f"\n开始下载 {model_name} 模型...")
    try:
        # 设置代理
        setup_proxy()
        
        # 创建一个使用系统证书的 HTTP 客户端
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where(),
            proxy_url='http://127.0.0.1:8118'
        )
        
        # 设置 SSL 上下文
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # 下载并加载模型
        with tqdm(unit='B', unit_scale=True, desc=f"下载 {model_name} 模型") as pbar:
            model = whisper.load_model(model_name)
            print(f"{model_name} 模型下载完成！")
        
        return True
    except Exception as e:
        print(f"下载 {model_name} 模型时出错: {str(e)}")
        print("尝试使用备用下载方式...")
        
        try:
            # 备用下载方式
            os.environ['CURL_CA_BUNDLE'] = certifi.where()
            model = whisper.load_model(model_name)
            print(f"{model_name} 模型下载完成！")
            return True
        except Exception as e2:
            print(f"备用下载方式也失败: {str(e2)}")
            return False

def main():
    """主函数"""
    # 要下载的模型列表
    models_to_download = ['small']  # 可以根据需要添加其他模型
    
    print("准备下载 Whisper 模型...")
    print("这可能需要几分钟时间，具体取决于您的网络速度。")
    
    success_count = 0
    for model_name in models_to_download:
        if download_model(model_name):
            success_count += 1
    
    total_models = len(models_to_download)
    if success_count == total_models:
        print("\n所有模型下载成功！")
        sys.exit(0)
    else:
        print(f"\n下载完成，但有 {total_models - success_count} 个模型下载失败。")
        print("请检查错误信息并重试。")
        sys.exit(1)

if __name__ == "__main__":
    main()
