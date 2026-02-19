from home.models import EmojiEffectConfig

def emoji_effect_config(request):
    config = EmojiEffectConfig.objects.first()
    if config:
        return {
            'emoji_effect_emoji': config.emoji,
            'emoji_effect_opacity': config.opacity,
        }
    return {
        'emoji_effect_emoji': '❄️',
        'emoji_effect_opacity': 1.0,
    }
