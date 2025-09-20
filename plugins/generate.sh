#!/usr/bin/env bash

lv2info -p amp.ttl 'http://github.com/mikeoliphant/neural-amp-modeler-lv2'
lv2info -p tonestack.ttl 'http://distrho.sf.net/plugins/3BandEQ'
lv2info -p cab.ttl 'http://moddevices.com/plugins/mod-devel/cabsim-IR-loader'
lv2info -p hallReverb.ttl https://github.com/michaelwillis/dragonfly-reverb
lv2info -p globalEq.ttl http://eq10q.sourceforge.net/eq/eq4qs 
lv2info -p sequencer.ttl http://gareus.org/oss/lv2/stepseq#s8n8
lv2info -p drumkit.ttl http://gareus.org/oss/lv2/avldrums#RedZeppelin


ttl2jsonld tonestack.ttl > tonestack.json
ttl2jsonld amp.ttl > amp.json
ttl2jsonld cab.ttl > cab.json
ttl2jsonld hallReverb.ttl > hallReverb.json
ttl2jsonld globalEq.ttl > globalEq.json
ttl2jsonld sequencer.ttl > sequencer.json
ttl2jsonld drumkit.ttl > drumkit.json