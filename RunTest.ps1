coverage run -m pytest
if ($?)
{
    coverage report -m
}
