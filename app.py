import os

from update_summarizer import (app, job_add_summary_token,
                               job_check_expire_dates, scheduler)

if __name__ == "__main__":
    scheduler.add_job(id='job_check_expire_dates',
    func=job_check_expire_dates, trigger='cron', day_of_week='mon-sun', hour=0, minute=1)
    scheduler.add_job(id='job_add_summary_token',
    func=job_add_summary_token, trigger='cron', day_of_week='mon-sun', hour=0, minute=1)
    app.run(debug=True, port=os.getenv("PORT") or 8080)