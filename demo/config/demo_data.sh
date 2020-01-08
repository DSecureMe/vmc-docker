echo "Ralph: Make migrations"
docker exec -it compose_web_1 ralphctl migrate

echo "Ralph: Load demo data  (login: ralph, password: ralph)"
docker exec -it compose_web_1 ralphctl demodata
docker exec -it compose_web_1 python3 /test_data/generate_ips.py

echo "VMC: Load data (superuser login: admin, password:adminadmin)"
docker exec -it compose_admin_1 vmc loaddata /tmp/demo_data.json

echo "VMC: Import Assets from Ralph"
docker exec -it compose_admin_1 vmc shell -c 'from vmc.ralph.tasks import load_all_assets; load_all_assets();'