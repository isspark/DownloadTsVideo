import os
import requests

session = requests.session()


def getM3u8(m3u8_url):
    try:
        m3u8 = session.get(m3u8_url)
        content_str = str(m3u8.content,encoding='utf-8').split('\n')
        ts_names = []
        for line in content_str:
            if not '.ts' in line:
                continue
            else:
                ts_names.append(line)
        return ts_names
    except Exception as error:
        print("get m3u8 error :",error)
        exit(1)


def getTs_url(m3u8_url,ts_names):
    ts_urls = []
    for ts_name in ts_names:
       ts_urls.append(url_m3u8.replace(m3u8_url.split('/')[-1], ts_name))
    return ts_urls;


def download_ts(ts_names, ts_urls, path):
    # ts = session.get('https://oss1898.aliyunsysfiles.com/hls/contents/videos/7000/7886/7886_hd_000.ts')
    # with open(ts_names[0],"wb") as code:
    #     code.write(ts.content)
    if len(ts_urls) <= 0:
        print("no video nedd download,skip it!")
        print('-----------------------end download file-----------------------')
        return False
    if len(ts_urls) >= 250:
        print("the video too large,skip it!")
        print('-----------------------end download file-----------------------')
        return False
    if not os.path.exists(path):
        os.mkdir(path)
    for ts_index, ts_url in enumerate(ts_urls):
        print(f'download file progress,url:{ts_url},total:{ts_index}/{len(ts_urls)}')
        ts = session.get(ts_url,stream=True,timeout=60)
        with open(f'{path}\{ts_names[ts_index]}',"wb+") as file:
            for chunk in ts.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
    return True


def merge_files(path,video_name):
    cmd = f'copy /b {path}\*.ts  {path}\{video_name}.mp4'
    print('execute cmd :',cmd)
    os.system(cmd)
    os.system(f'del {path}\*.ts')  # 调用windows命令行（即cmd）工具，运行命令
    print(f'{video_name}.mp4 finish down!')


if __name__ == '__main__':
    download_num = 500;
    start_num = 7756;
    for x in range(download_num):
        num = start_num - x - 1
        url_m3u8 = f'https:/hls/contents/videos/7000/{num}/{num}_hd.m3u8'
        videoName = url_m3u8.split('/')[-2]
        print('start vidoe: ',videoName)
        path = f'E:\Movie\Study\\{num}'
        ts_names = getM3u8(url_m3u8)
        print('download m3u8 success!')
        ts_urls = getTs_url(url_m3u8,ts_names)
        print('-----------------------start download file-----------------------')
        download_result = download_ts(ts_names,ts_urls,path)
        print('-----------------------end download file-----------------------')
        print('-----------------------start merge file-----------------------')
        if download_result: 
            merge_files(path, videoName)
        print('-----------------------end merge file-----------------------')
        
