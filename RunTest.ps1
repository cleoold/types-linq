coverage run -m pytest @args
if ($?)
{
    coverage report -m
}
