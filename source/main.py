import json
import os
import shutil
from loguru import logger
from tester import Tester


def clear_temp_folder():
    folder_path = '../outputs/temp'
    if os.path.exists(folder_path):
        for f in os.listdir(folder_path):
            file_path = os.path.join(folder_path, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    logger.info("outputs/temp folder has been cleared.")


def main():

    logger.add('../outputs/log/{time:YYYY-MM-DD}.log', rotation='1 day', level="INFO")
    logger.info("---------------This is a new start------------------")
    tester = Tester(path='../inputs/config.json', logger=logger)

    # ToDo Test
    tester.run()
    tester.process_data()

    logger.info("---------------END------------------")


if __name__ == "__main__":
    main()

"""

    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description="这是一个仿真器性能测试软件")
    parser.add_argument('-i', '--input', nargs='+', help='请输入一个json文件的路径作为仿真的配置文件',
                        default="./inputs/config.json")
    parser.add_argument('-c', '--clear', action='store_true', help='清理temp文件夹')

    logger.add('outputs/log/{time:YYYY-MM-DD}.log', rotation='1 day', level="INFO")
    logger.info("---------------This is a new start------------------")

    if parser.parse_args().input:
        input_path = parser.parse_args().input[0]
    elif parser.parse_args().clear:
        clear_temp_folder()
        logger.info("temp folder have been cleared.")
        return
"""