source smd_0_push.sh

python extract_json_ntg.py \
	${SMDATA_DIR}/raw/${1} \
	${SMDATA_DIR}/json_raw_ntg/${1} \
	${2}
