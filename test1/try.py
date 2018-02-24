rooturl='http://www.eisenwarenmesse.com'

totalpages=136
pagesize=20

for i in range(20,20*137,20):
    starturl='%s/IEM/Exhibitor-search/index.php?fw_goto=aussteller/blaettern&&start=%s&paginatevalues={"stichwort":""}' % (rooturl, i)
    print starturl