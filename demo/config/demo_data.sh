echo "Ralph: Make migrations"
docker exec -it compose_web_1 ralphctl migrate

echo "Ralph: Load demo data  (login: ralph, password: ralph)"
docker exec -it compose_web_1 ralphctl demodata
docker exec -it compose_web_1 python3 /test_data/generate_ips.py

echo "Elastalert: Create Indexes"
#docker exec -it compose_elastalert_1 /usr/bin/elastalert-create-index --config /opt/elastalert/config.yaml

echo "HIVE: create database (superuser login: admin, password: admin)"
#docker exec -it compose_hive_elasticsearch_1 chmod +x /test_data/load.sh
#docker exec -it compose_hive_elasticsearch_1 /test_data/load.sh

echo "VMC: Load data (superuser login: admin, password: adminadmin)"
docker exec -it compose_admin_1 vmc loaddata /test_data/demo_data.json
docker exec -it compose_admin_1 vmc create_index

echo "Kibana: Import Sample Dashboards and KPIs"
#docker exec -it compose_kibana_1 chmod +x /test_data/load.sh
#docker exec -it compose_kibana_1 /test_data/load.sh

echo "VMC: Prepare demo data"
docker exec -it compose_admin_1 python3 -W ignore /test_data/generate_vulns.py