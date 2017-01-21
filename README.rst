============
TSV to motor
============

-----------
Description
-----------

This is a simple python script for converting a table of samples information into a `motor`_ script.

The table should be in tab-separated value format structured like this:

+----------+------+------------+------------+------------+-----------+-------+-----------------+
| compound | edge | x-position | y-position | z-position | scan name | scans | comment         |
+==========+======+============+============+============+===========+=======+=================+
| Li2C2Te  | Te   | 7500       | -51718.5   | 124000     | xafs      | 2     | Glass capillary |
+----------+------+------------+------------+------------+-----------+-------+-----------------+

See `input.tsv`_ for a full example.

.. _motor: http://mx.iit.edu/
.. _input.tsv: ./input.tsv

-------------
Example usage
-------------

::

    $ python tsv-to-motor.py input.tsv

This will produce a file in the current directory called ``input.tsv_motor_script.txt`` which can be executed from motor::

   motor> @input.tsv_motor_script.txt

or::

   motor> exec input.tsv_motor_script.txt

-------
License
-------

This project is licensed under the terms of the `MIT license`_.

.. _MIT license: LICENSE.txt
