
# vim: set ft=python:
import os, os.path
env = Environment( )

import openaps

def recipe_scanner (node, env, path):
  lines = [ os.path.basename(l.strip( )) for l in node.get_contents( ).split('\n') \
            if l.strip( ) and not l.strip( ).startswith('#') ]
  out = [ ]
  for dep in lines:
    env.AlwaysBuild(env.Report(dep, []))
    out.append(env.File(dep))
  return out

ReportList = Scanner(function = recipe_scanner,
                      skeys = ['.openaps'])

Report = Builder(action="""
  openaps report invoke $TARGET
  """)

def phase_targets (target, source, env):
  return target, source

Phase = Builder(action = """
  echo $TARGETS -- $SOURCES
  """, src_suffix = '.openaps',
  emitter = phase_targets)

env.Append(SCANNERS=ReportList)
env.Append(BUILDERS = { 'Phase': Phase, 'Report': Report })

env.Phase(Glob('*.openaps'))

