#! /bin/bash

nginx_dir="/etc/nginx/conf.d"
dest_certs_dir="/etc/ssl/letsencrypt"
source_certs_dir="/home/user-data/ssl"

cur_dir=`pwd`

# domains=()

# cd $nginx_dir

# for domain in `ls 10.*`
# do
#     domains+=( ${domain:3:-5} )
# done

cd $source_certs_dir

domains=`ls *.pem | grep -vE '^(ssl_certificate|ssl_private_key|dh2048).pem$' | sed -e 's/-.*//' | uniq`

for domain in $domains
do
    domain_cert=`ls -1t $domain*.pem | head -n 1`
    domains_cert=`openssl x509 -in $domain_cert -text -noout | grep DNS: | sed -e 's/^[[:space:]]*/ /' | tr ',' '\n' | cut -c 6- | grep -vE '^(autoconfig|autodiscover|www)\.'`
    for name in $domains_cert
    do
        cp $source_certs_dir/$domain_cert $dest_certs_dir/$name.pem
    done

    # domain_cert=""
    # domain_cert=`ls -1t $domain*.pem | head -n 1` || true
    # if [ "$domain_cert" = "" ]
    # then
    #     domain_cert=ssl_certificate.pem
    # fi
    # cp $source_certs_dir/$domain_cert $dest_certs_dir/$domain.pem
done

cp ssl_private_key.pem $dest_certs_dir/
# cp ssl_certificate.pem $dest_certs_dir/

cd $cur_dir

/etc/init.d/nginx reload
