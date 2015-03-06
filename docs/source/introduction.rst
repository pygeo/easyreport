Introduction
============

SmartReport is a template based engine to generate reports in multiple output formats based on very flexible input.

Let us assume that you have a program which produces a lot of figures, statistics and other output. you want to present these results in a nice way and have full flexibility to allow for different output formats, like e.g. HTML, PDF and others. One solution to this might be that you generate your output directly from your program. Fine with that. Tools like e.g. <`markup.py` http://markup.sourceforge.net/>_ are very helpfull here.

However, could you imagine that the results of your code are also coming from *parallel processes*? If so, then generating a report from these results would be quite difficult.

**SmartReport aims to completely separate the processing and the reporting**. You can use it in a flexible way to generate reports based on arbitrary output. As it is based on templates it is highly customizable.


Objective
---------

Major objectives are

* support reporting based on results from parallel processing
* support user based templates for customized report generation
* allow for flexible integration of report generating engines like e.g. Sphinx to maximize flexibility in output formats
* separate as much as possible the content from the actual format
* independency from code which generate the output

Philosophy
----------

To achieve the above objectives, smartreport uses templates and separates the content and the format. The main steps to be undertaken when generating a report from arbitrary output are

1. gather information
2. structure this information based on user template
3. generate report in user defined output format

Example
-------

Let's give first an application example. Let's say you have a program, which you runs three processes (A,B,C) in parallel. All the processes are writing output (graphics, statistics) to a particular output directory.

Thus in the end you end up with something like this::

    /<some dir>/
               /A1.png
               /B1.png
               /C1.png
               /A1.gif
               /B1.gif
               /C1.gif
               /a.csv
               /b.csv
               /c.csv

You end up with lots of files, some of them are graphics, some of them are textfiles. What a mess, how could you structure and present your results? You need a *smart* way to do that. Here you go.

Define a template
~~~~~~~~~~~~~~~~~

Let's say you want your results to be organized in `restructured text <http://en.wikipedia.org/wiki/ReStructuredText>`_ syntax (In principle it could be any format that can be written in a plain ASCII file). What you would typically do is to write a report yourself as follows::

    Result A
    --------
    blablablabla blabla blabla

    .. figure:: images/A1.png
       :scale: 50 %

       This is the caption of figure A1.png

    blablabla

    statistic a.csv here

    blablabla

    .. figure:: images/A1.gif
       :scale: 50 %

       This is the caption of figure A1.gif

    Result B
    --------
    blablablabla blabla blabla

    .. figure:: images/B1.png
       :scale: 50 %

       This is the caption of figure B1.png

    blablabla

    statistic b.csv here

    blablabla

    .. figure:: images/B1.gif
       :scale: 50 %

       This is the caption of figure B1.gif

Let us now assume that you have not results from 3 operations, but from 20 or even more. Wouldn't it be nice to have some more automated approach to the report generation, which gives you nevertheless the flexibility to easily adapt the look-and-feel? Let's make a template from the above::

<<ITER source=root, key=VAR>>
    Result <<VAR.name>>
    --------
    blablablabla blabla blabla

    .. figure:: <<VAR.files.northern>>
       :scale: 50 %

       <<VAR.files.northern.file>>

    blablabla

    statistic <<VAR.statfile>> here

    <<ITER source=VAR.observations, key=OBS>>
    Observation
    ~~~~~~~~~~~
    blablabla

    .. figure:: <<OBS.name>>
       :scale: 50 %

       This is the caption of figure <<OBS.filename>>   <<- replace this with MAKOTEMPLATES
    <</ITER>>

<</ITER>>


You see that we have replaced in the above code some of the content by variables, which are indicated by tags. These tags can be arbitrary strings and are enclosed by '<<' and '>>'.

**Recipie to generate a template**

1. write the text like you would do it by hand
2. replace components which you like to be flexible by hand
3. define sections on which you would like to have itteration capabilities by adding controling structures based on the `makotemplate syntax <http://www.makotemplates.org/>`_.



This file needs to be written at the end of the processing based on the project_info information!

Models:
- name : my_model_A
  institute : MPI-M
  files:
    northern:
       file : A.png
       caption : My test caption for nothern hemisphere
    southern :
       file : B.png
       caption : My test caption for southern hemisphere
   observations:
      - name : GlobAlbedo
        filename : 'obsA1.png'
   statfile : a.csv


 - B.png
   caption : caption for B

- name: a
  value: 1
- name: b
  value: 2


Current Limitations and ideas
-------------------

* SPHINX is currently called from the command line. This can be done better using Sphinx builder class
* develop template files for different kind of usecases --> user should invest as less time as possible into understanding makotemplates
* SPHINX layout based on default setup, allow users to specify customized setup
* implement classes on that allow user to easily register data and write final YAML file
* implement a help routine that writes code smippets already in a way the user might need them
* handling of images; links as perspective


