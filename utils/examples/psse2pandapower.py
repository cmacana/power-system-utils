import grg_pssedata as grg

case = grg.io.parse_psse_case_file("/utils/psse/minimal_exampleV33.raw")
for v in case.buses:
    print(v.vm)