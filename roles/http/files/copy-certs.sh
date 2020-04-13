#! /bin/sh

nginx_dir="/etc/nginx/conf.d"
dest_certs_dir="/etc/ssl/letsencrypt"
source_certs_dir="/home/user-data/ssl"

cur_dir=`pwd`

domains=()

cd $nginx_dir

for domain in `ls 10.*`
do
    domains+=( ${domain:3:-5} )
done

cd $source_certs_dir

for domain in $domains
do
    domain_cert=`ls -1t $domain*.pem | head -n 1`
    cp $source_certs_dir/$domain_cert $dest_certs_dir/$domain.pem
done

cp ssl_private_key.pem $dest_certs_dir/

cd $cur_dir

/etc/init.d/nginx reload
