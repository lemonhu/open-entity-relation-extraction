import json
import traceback

class AppendToJson:
    """将抽取得到的Json格式的知识三元组添加写入Json文件"""

    def append(self, file_path, knowledge):
        """添加到Json文件
        Args:
            file_path: string，Json文件路径
            knowledge: dict，抽取出的知识
        Returns:
        """
        with open(file_path, 'a', encoding='utf-8') as f_out:
            try:
                f_out.write(json.dumps(knowledge, ensure_ascii=False))
                f_out.write('\n')
                f_out.flush()
            except Exception as e:
                traceback.print_exc()
                raise e
            finally:
                f_out.close()
