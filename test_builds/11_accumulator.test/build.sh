set -e

source config.sh

sudo $P4APP_PATH build .

echo
echo " BMV2 BUILD SUCCEDED "
echo

export P4C_BIN_DIR=$P4C_BIN_DIR
$NFP4BUILD_PATH -p out/ -o simple_router.nffw -l $NFPTARGET -4 main.p4 --nfp4c_p4_version 16 \
--nfp4c_D TARGET_NFP --nfp4c_D PIF_GLOBAL_FLOWCACHE_DISABLED --disable-component flowcache -DPIF_GLOBAL_FLOWCACHE_DISABLED \
--nfp4c_p4_compiler p4c-nfp  --no-shared-codestore --disable-component flowcache -I /opt/netronome/p4/components/flowcache/me/lib/flowcache/ \
--nfp4c_I /opt/netronome/p4/components/flowcache/me/lib/flowcache/




echo
echo " NFP BUILD SUCCEDED "
echo
