from apscheduler.schedulers.blocking import BlockingScheduler

def my_job():
    print("定时任务执行了！")

if __name__ == "__main__":
    
    scheduler = BlockingScheduler()
    # 每隔5秒执行一次my_job函数
    scheduler.add_job(my_job, 'interval', seconds=5)
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
