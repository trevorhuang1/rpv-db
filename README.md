# RPV steel irradiation mini-database

This is a small SQLite database of public reactor pressure vessel (RPV) steel irradiation data, built to keep the measurements tied to each unique material, source, and also how noisy the data is. I built this to practice my database skills after a break from coding.

## Source

Jacobs, Yamamoto, Odette, Morgan, "Dataset RPV TTS 1.0", Materials Data Facility, doi:10.18126/3zkm-yd51 (2023). Paper: Materials & Design 236, 112491. I couldn't find a license on the dataset page, so I didn't publish the raw xlsx to this repo.

## Notes on the xlsx file

Each row consists of one transition temperature shift (delta T41J), six chemistry values (wt% Cu, Ni, Mn, P, Si, C), irradiation temperature, log10 fluence (n/cm^2), log10 flux (n/cm^2/s), and a `datatype` label for the dataset it came from.

## How data is stored

I created 3 tables within my database, which are defined in `models.py`:

1. `sources`: one row per `datatype` label, which descriptions of the unique sources and the DOI.
2. `materials`: one row per distinct composition of material
3. `results`: Each test, linked to one source and one material and it's raw location in the xlsx file

Column names were renamed so that units could be included. 

I treated rows with identical composition as the same material, but this may not be the case due to differences in annealing/work hardening.

## Find noise from repeat measurements

`noise.py` groups rows with the same source, composition, temperature, flux, and fluence and compares the shift. 

I found an overall pooled SD of 8.2 degrees Celsius, whic hmeans two measurements under identical conditions typically differ by several degrees Celsius. This would be important to keep in mind if it was used to train a model.

## How to run it

1. Create a virtual environment by running `. venv.sh`
2. Download the dataset and put it in `data/raw` (it is not committed as of now)
3. Run `python load_db.py` to build `rpv.db`, which contain the 3 tables
4. Run `python noise.py` to print the noise data table

## Credits

- `models.py` was adapted from NighthawkCodingSociety's flask_2025 and updated in vanilla SQLalchemy (link: https://github.com/nighthawkcoders/flask_2025)
- Data: see source