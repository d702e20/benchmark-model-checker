# bench-solver

Running on Mexican Standoff thrice:
```
Running: cd ../OnTheFlyATL/ && cargo run --package atl-checker --bin atl-checker -- solver --formula benches/lcgs/Mexican_Standoff/Mexican_Standoff_p1_is_alive_till_he_aint.json --model benches/lcgs/Mexican_Standoff/Mexican_Standoff.lcgs --model-type lcgs
wall time: 0.20350737999251578, usertime: 0.904412, systime: 0.076476, peak 22824 KiB
Running: cd ../OnTheFlyATL/ && cargo run --package atl-checker --bin atl-checker -- solver --formula benches/lcgs/Mexican_Standoff/Mexican_Standoff_p1_is_alive_till_he_aint.json --model benches/lcgs/Mexican_Standoff/Mexican_Standoff.lcgs --model-type lcgs
wall time: 0.23878169899398927, usertime: 2.070686, systime: 0.126034, peak 23008 KiB
Running: cd ../OnTheFlyATL/ && cargo run --package atl-checker --bin atl-checker -- solver --formula benches/lcgs/Mexican_Standoff/Mexican_Standoff_p1_is_alive_till_he_aint.json --model benches/lcgs/Mexican_Standoff/Mexican_Standoff.lcgs --model-type lcgs
wall time: 0.24613207500078715, usertime: 3.637086, systime: 0.220474, peak 23008 KiB

Results: Over 3 runs; avg walltime: 0.2295, avg usertime: 2.2041, avg systime: 0.1410, max peak 23008 KiB
```
