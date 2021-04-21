import grg_pssedata as grg

case = grg.io.parse_psse_case_file("/psutils/psse/minimal_exampleV33.raw")
for v in case.buses:
    print(v.vm)