echo "Ralph: Make migrations"
docker exec -it compose_web_1 ralphctl migrate

echo "Ralph: Load demo data  (login: ralph, password: ralph)"
docker exec -it compose_web_1 ralphctl demodata
docker exec -it compose_web_1 python3 /test_data/generate_ips.py

echo "VMC: Load data (superuser login: admin, password:adminadmin)"
docker exec -it compose_admin_1 vmc loaddata /test_data/demo_data.json

echo "Kibana: Import Sample Dashboards and KPIs"
docker exec -it compose_kibana_1 /test_data/load.sh

echo "VMC: Import Assets from Ralph"
docker exec -it compose_admin_1 python3 -W ignore /test_data/generate_vulns.py

echo "Done"