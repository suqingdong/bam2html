=========
Tutorials
=========


``highlight single position``
=============================

.. code:: console

    bam2html -b demo.bam 1:12345
    bam2html -b demo.bam 1:12345 2:45678


``highlight multiple positions in one file``
============================================

.. code:: console

    bam2html -b demo.bam 1:12345,12347
    bam2html -b demo.bam 1:12345,12349 2:45678,45681


``highlight a region``
======================

.. code:: console

    bam2html -b demo.bam 1:12345-12350


``highlight in batch mode``
===========================

.. code:: console

    # multiple bams separated by comma
    bam2html -b demo.bam,demo2.bam 1:12345 2:34567

    # multiple bams in a file(one bam per line)
    bam2html -bl bam.list 1:12345 2:34567

    # multiple positions in a file
    bam2html -bl bam.list pos.list

    # generate summary.html
    bam2html -bl bam.list pos.list -s

    # compress the result
    bam2html -bl bam.list pos.list -s -x zip
    bam2html -bl bam.list pos.list -s -x tar.gz
