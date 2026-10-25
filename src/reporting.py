from collections import Counter


def summarise_analysis(results: list[dict]) -> dict:
    if not results:
        return {'frames_analysed':0,'movement_counts':{},'averages':{}}
    movements = Counter(item['movement'] for item in results)
    numeric = ['left_knee_angle','right_knee_angle','hip_angle','torso_lean','stride','balance']
    averages = {}
    for key in numeric:
        values = [float(item['metrics'][key]) for item in results if key in item['metrics']]
        if values:
            averages[key] = round(sum(values)/len(values), 2)
    speed_keys = ['horizontal_speed','vertical_speed','ankle_speed']
    for key in speed_keys:
        values = [abs(float(item[key])) for item in results]
        averages[key] = round(sum(values)/len(values), 3)
    dominant = movements.most_common(1)[0][0]
    return {
        'frames_analysed': len(results),
        'dominant_movement': dominant,
        'movement_counts': dict(movements),
        'averages': averages,
        'coaching_notes': coaching_notes(averages, movements),
    }


def coaching_notes(averages: dict, movements: Counter) -> list[str]:
    notes = []
    if averages.get('balance', 1) < .7:
        notes.append('Balance proxy was lower across the sampled sequence; review centre-of-mass control with a coach.')
    if averages.get('torso_lean', 0) > 35:
        notes.append('Average torso lean was high; inspect whether this is intentional for the movement phase.')
    if movements.get('SPRINTING',0) or movements.get('RUNNING',0):
        notes.append('Running phases were detected; compare stride and knee-angle trends across repeated drills.')
    if movements.get('KICKING',0):
        notes.append('Kicking phases were detected; inspect supporting-leg knee angle and balance around contact.')
    if not notes:
        notes.append('No major rule-based posture flags were triggered in the analysed frames.')
    return notes


def to_markdown(summary: dict, source_name: str = 'session') -> str:
    lines = [f'# Player Performance Report — {source_name}', '', f"Frames analysed: **{summary.get('frames_analysed',0)}**", f"Dominant movement: **{summary.get('dominant_movement','N/A')}**", '', '## Movement counts']
    lines += [f"- {k}: {v}" for k,v in summary.get('movement_counts',{}).items()]
    lines += ['', '## Average metrics'] + [f"- {k}: {v}" for k,v in summary.get('averages',{}).items()]
    lines += ['', '## Coaching notes'] + [f"- {n}" for n in summary.get('coaching_notes',[])]
    lines += ['', '> Educational sports-analytics output; not a medical or injury diagnosis.']
    return '\n'.join(lines)
