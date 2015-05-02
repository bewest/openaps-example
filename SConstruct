
# vim: set ft=python:
import os, os.path
env = Environment( )

import openaps

def monitor_scanner (node, env, path):
  lines = [ os.path.basename(l.strip( )) for l in node.get_contents( ).split('\n') \
            if l.strip( ) and not l.strip( ).startswith('#') ]
  out = [ ]
  for dep in lines:
    print dep, node, path
    # env.Command(dep, node, """ openaps report invoke $TARGET """)
    # env.SideEffect(dep, node)
    env.AlwaysBuild(env.Report(dep, []))
    out.append(env.File(dep))
  return out
  return lines

MonitorList = Scanner(function = monitor_scanner,
                      skeys = ['.openaps'])

env.Append(SCANNERS=MonitorList)


Report = Builder(action="""
  openaps report invoke $TARGET
  """)

def phase_targets (target, source, env):
  print "emitting", str(target[0]), str(source), env
  return target, source

Phase = Builder(action = """
  echo $TARGETS -- $SOURCES
  """, src_suffix = '.openaps',
  target_scanner = MonitorList,
  emitter = phase_targets)

env.Append(BUILDERS = { 'Phase': Phase, 'Report': Report })

env.Phase(Glob('*.openaps'))



