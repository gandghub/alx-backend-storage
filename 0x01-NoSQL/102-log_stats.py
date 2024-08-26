#!/usr/bin/env python3
""" Log stats """
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db_nginx = client.logs.nginx
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    # Count total logs
    count_logs = db_nginx.count_documents({})
    print(f'{count_logs} logs')

    # Count logs per method
    print('Methods:')
    for method in methods:
        count_method = db_nginx.count_documents({'method': method})
        print(f'\tmethod {method}: {count_method}')

    # Count GET requests to /status
    check = db_nginx.count_documents({"method": "GET", "path": "/status"})
    print(f'{check} status check')

    # Top 10 most common IPs
    print("IPs:")
    ips = db_nginx.aggregate([
        {"$group": {
            "_id": "$ip",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])

    for ip in ips:
        print(f"\t{ip['ip']}: {ip['count']}")
