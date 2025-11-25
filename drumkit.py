class DrumKit:
    Kick = 36
    Snare = 38
    HiHat = 42

    KickSequence = 1
    SnareSequence = 2
    HiHatSequence = 3

    def __init__(self, sequencer):
        # Sequencery / Drum Track
        sequencer.param('drummode', 1) # change to drum sequencing, otherwise not all events are fired
        sequencer.param('sync', 1) # Sync to host (mod)
        sequencer.param('div', 2) # 8th

        sequencer.param(f'note{DrumKit.KickSequence}', DrumKit.Kick)
        sequencer.param(f'note{DrumKit.SnareSequence}', DrumKit.Snare)
        sequencer.param(f'note{DrumKit.HiHatSequence}', DrumKit.HiHat)


        self.sequencer = sequencer

    def set_velocities(self, sequence, velocities):
        for i, vel in enumerate(velocities):
            self.sequencer.param(f'grid_{i+1}_{sequence}', vel)
    def set_kick(self, velocities):
        self.set_velocities(DrumKit.KickSequence, velocities)
    def set_snare(self, velocities):
        self.set_velocities(DrumKit.SnareSequence, velocities)
    def set_hihat(self, velocities):
        self.set_velocities(DrumKit.HiHatSequence, velocities)  