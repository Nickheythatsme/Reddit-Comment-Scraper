@ECHO off

SET client_id='DWgIcrR8lKPqrg'
SET client_secret='hbsFxEyUyuvm01yFzkttQeK990w'
SET user_agent='pull comments from reddit and analyze them'
if exist python3 (
    python3 main.py
)else (
    python main.py
)
