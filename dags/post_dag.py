from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from jingritoutiao import post_article

# from airflow.operators.dummy_operator import DummyOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 1),
    "email": ["example@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# 每天凌晨5点运行
with DAG(
    "post_article_task",
    default_args=default_args,
    description="A simple DAG that runs every day at 5 AM",
    schedule_interval="0 5 * * *",
    catchup=False,
) as dag:

    # start_task = DummyOperator(task_id="start_task")
    title = "今日头条Airflow文章"
    content = """
　　中国共产党是中国工人阶级的先锋队，同时是中国人民和中华民族的先锋队，是中国特色社会主义事业的领导核心，代表中国先进生产力的发展要求，代表中国先进文化的前进方向，代表中国最广大人民的根本利益。党的最高理想和最终目标是实现共产主义。
　　中国共产党以马克思列宁主义、毛泽东思想、邓小平理论、“三个代表”重要思想、科学发展观、习近平新时代中国特色社会主义思想作为自己的行动指南。
　　马克思列宁主义揭示了人类社会历史发展的规律，它的基本原理是正确的，具有强大的生命力。中国共产党人追求的共产主义最高理想，只有在社会主义社会充分发展和高度发达的基础上才能实现。社会主义制度的发展和完善是一个长期的历史过程。坚持马克思列宁主义的基本原理，走中国人民自愿选择的适合中国国情的道路，中国的社会主义事业必将取得最终的胜利。
　　以毛泽东同志为主要代表的中国共产党人，把马克思列宁主义的基本原理同中国革命的具体实践结合起来，创立了毛泽东思想。毛泽东思想是马克思列宁主义在中国的运用和发展，是被实践证明了的关于中国革命和建设的正确的理论原则和经验总结，是中国共产党集体智慧的结晶。在毛泽东思想指引下，中国共产党领导全国各族人民，经过长期的反对帝国主义、封建主义、官僚资本主义的革命斗争，取得了新民主主义革命的胜利，建立了人民民主专政的中华人民共和国；新中国成立以后，顺利地进行了社会主义改造，完成了从新民主主义到社会主义的过渡，确立了社会主义基本制度，发展了社会主义的经济、政治和文化。
　　十一届三中全会以来，以邓小平同志为主要代表的中国共产党人，总结新中国成立以来正反两方面的经验，解放思想，实事求是，实现全党工作中心向经济建设的转移，实行改革开放，开辟了社会主义事业发展的新时期，逐步形成了建设中国特色社会主义的路线、方针、政策，阐明了在中国建设社会主义、巩固和发展社会主义的基本问题，创立了邓小平理论。邓小平理论是马克思列宁主义的基本原理同当代中国实践和时代特征相结合的产物，是毛泽东思想在新的历史条件下的继承和发展，是马克思主义在中国发展的新阶段，是当代中国的马克思主义，是中国共产党集体智慧的结晶，引导着我国社会主义现代化事业不断前进。"""

    post_article_task = PythonOperator(
        task_id="post_article_task",
        python_callable=post_article,
        op_kwargs={
            "title": title,
            "content": content,
        },
    )
