import time
from src.graph import WorkFlow

CHECK_INTERVAL = 180  # 3 minutes


def run():
    print("🚀 Email Automation Service Started")
    print(f"⏱ Check interval: {CHECK_INTERVAL} seconds\n")

    app = WorkFlow().app
    checked_ids = []

    while True:
        try:
            print("🔄 Starting new automation cycle...\n")

            result = app.invoke({
                "checked_emails_ids": checked_ids,
                "emails": [],
                "action_required_emails": []
            })

            # Save processed ids
            checked_ids = result.get("checked_emails_ids", checked_ids)

            print(f"\n⏳ Waiting {CHECK_INTERVAL} seconds...\n")
            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print("\n❌ Error occurred:")
            print(e)
            print("\n🔁 Retrying in 30 seconds...\n")
            time.sleep(30)


# 🔥 THIS WAS PROBABLY REMOVED
if __name__ == "__main__":
    run()