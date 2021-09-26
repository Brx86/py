import threadpool

ef run_get_fusion_mongo_result(doc_id):
    global temp_result
    print doc_id
    db_facetValues=get_organization_facet_count(doc_id)
    db_facetValues.sort()
    print 'db_facetValues',db_facetValues
    fusion_facetValues=get_fusion_data(doc_id)
    fusion_facetValues.sort()
    print 'fusion_facetValues',fusion_facetValues
    diff = list(set(db_facetValues).difference(set(fusion_facetValues)))
    temp_result_docid = {}
    if diff:
        temp_result_docid['PublicationId'] = doc_id
        temp_result_docid['Diff_Facets'] = diff
    if mutex.acquire(1):
        if temp_result_docid:
            temp_result.append(temp_result_docid)
        mutex.release()