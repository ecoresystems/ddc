source var.sh

for COLL in fraxtil itg
do
	./smd_ntg_1_extract.sh ${COLL} --itg
done

for COLL in fraxtil itg
do
	./smd_ntg_2_filter.sh ${COLL}
done

./smd_ntg_3_export.sh
