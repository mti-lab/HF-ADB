import os
import re
import logging
import argparse

def setup_logger(dir):
    logger = logging.basicConfig(filename=os.path.join(dir, "sammary.log"), level=logging.INFO)
    return logger

def main(experiment_name, log_dir, output_dir, is_input):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("logger")

    overall_result = {}

    for method in os.listdir(log_dir):
        if not os.path.isdir(os.path.join(log_dir, method)):
            continue
        sum_score = [0, 0, 0, 0]
        if method == "adversarial":
            sum_score.append(0)
            sum_score.append(0)
        cnt = 0
        for sample_id in os.listdir(os.path.join(log_dir, method)):
            if not os.path.isdir(os.path.join(log_dir, method, sample_id)):
                continue
            # ログファイルを読み込む
            with open(os.path.join(log_dir, method, sample_id, "evaluation.log"), 'r') as log_file:
                log_content = log_file.read()

            # 正規表現を使って平均スコアを抜き出す
            pattern = re.compile(r'average score: (\d+\.\d+)')
            matches = pattern.findall(log_content)
            scores = [float(match) for match in matches]

            # 抜き出した平均スコアをリストで返す
            sum_score = [a + b for a, b, in zip(scores, sum_score)]

            cnt += 1

        scores = [a / cnt for a in sum_score]
        print(scores)

        handler = logging.FileHandler(os.path.join(log_dir, method,  "sammary.log"), mode='w')
        logger.addHandler(handler)
        logger.info(f"fdfr: {scores[0]}")
        logger.info(f"ism: {scores[1]}")
        logger.info(f"ser-fiq: {scores[2]}")
        logger.info(f"brisque: {scores[3]}")
        if method == "adversarial" and is_input == "true":
            logger.info(f"l_1: {scores[4]}")
            logger.info(f"l_2: {scores[5]}")
        logger.removeHandler(handler)

        result = {}
        result["fdfr"] = scores[0]
        result["ism"] = scores[1]
        result["ser-fiq"] = scores[2]
        result["brisque"] = scores[3]
        if method == "adversarial" and is_input == "true":
            result["l_1"] = scores[4]
            result["l_2"] = scores[5]

        overall_result[method] = result

    handler = logging.FileHandler(os.path.join(output_dir, "sammary.log"), mode='w')
    logger.addHandler(handler)
    logger.info(f"{experiment_name} overall results")
    for method in overall_result.keys():
        logger.info(f"---{method}---")
        for metric in overall_result[method].keys():
            logger.info(f"{metric}: {overall_result[method][metric]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='summerize result')
    parser.add_argument('--experiment_name', type=str, default=None)
    parser.add_argument('--log_dir', type=str, default=None)
    parser.add_argument('--output_dir', type=str, default=None)
    parser.add_argument('--is_input', type=str, default="false")
    args = parser.parse_args()
    main(args.experiment_name, args.log_dir, args.output_dir, args.is_input)
