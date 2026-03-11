from core.normalizer import normalize
from core.extractor import extract_coords, extract_quantity
from core.resolver import Resolver
from core.loader import load_list
import re


def route(text, classifier, engine, resolver, memory):
    intent = classifier.classify(text)

    if intent == "command":
        original_text = text
        item = resolver.resolve(text)
        text = normalize(text)
        coords = extract_coords(text)
        qty = extract_quantity(text)
        
        structures = load_list("data/structures.txt")
        structure_names = [s.replace("minecraft:", "") for s in structures]
        
        command_name = None
        for cmd in engine.commands:
            if cmd in text:
                command_name = cmd
                break
        
        text_lower = text.lower()
        
        structure_variants = {
            "village": ["village", "village_desert", "village_plains", "village_savanna", "village_snowy", "village_taiga"],
            "ruined_portal": ["ruined_portal", "ruined_portal_desert", "ruined_portal_jungle", "ruined_portal_mountain", "ruined_portal_nether", "ruined_portal_ocean", "ruined_portal_swamp"],
            "ocean_ruin": ["ocean_ruin_cold", "ocean_ruin_warm"],
            "shipwreck": ["shipwreck", "shipwreck_beached"],
            "mineshaft": ["mineshaft", "mineshaft_mesa"],
        }
        
        command_name = None
        for cmd in engine.commands:
            if cmd in text:
                command_name = cmd
                break
        
        if not command_name:
            if any(kw in text_lower for kw in ["find", "search", "nearest", "where", "locate all"]):
                for base_name, variants in structure_variants.items():
                    if base_name in text_lower or any(v.replace("_", " ") in text_lower or v.replace("_", "") in text_lower.replace(" ", "") for v in variants):
                        command_name = "locate"
                        result = f"=== FINDING NEAREST {base_name.upper().replace('_', ' ')} ===\n\n"
                        if memory.last_location:
                            result += f"Your current position: {memory.last_location}\n\n"
                        
                        result += "Step 1 - Get your exact coords:\n"
                        result += "/execute in minecraft:overworld run query entity @s pos\n\n"
                        result += f"Step 2 - Run ALL these locate commands:\n"
                        for i, v in enumerate(variants, 1):
                            result += f"{i}. /locate {v}\n"
                        result += "\nStep 3 - Calculate distance for each result:\n"
                        result += "In chat, compare distances and pick the nearest.\n\n"
                        result += "Step 4 - Teleport to nearest:\n"
                        result += "/tp @s <x> <y> <z>"
                        return {"type": "command", "result": result}
        
        if not command_name:
            if item:
                command_name = "give"
            else:
                return {"type": "chat", "result": "I didn't understand that. Try something like 'give me diamonds' or 'tp me to spawn'."}
        
        params = {}

        if item and command_name == "give":
            params["item"] = item
            params["count"] = qty
            memory.remember_item(item)
            params["player"] = "@s"

        if coords and command_name != "give":
            params["x"], params["y"], params["z"] = coords
            memory.remember_location(*coords)

        if "player" in engine.commands.get(command_name, ""):
            if command_name != "give":
                exclude_words = {"stack", "stacks", "of", "the", "a", "an", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "give", "me", "to", "with", "for"}
                text_parts = original_text.lower().split(command_name)[-1].split()
                player_candidates = [w for w in text_parts if w not in exclude_words and len(w) > 1 and not w.isdigit()]
                if player_candidates:
                    player = player_candidates[0]
                    if player not in ["me", "spawn", "home"]:
                        params["player"] = player
                    else:
                        params["player"] = "@s"
                else:
                    params["player"] = "@s"

        if command_name == "tp" and not coords:
            if "spawn" in text:
                params["x"], params["y"], params["z"] = "0", "64", "0"
            elif "home" in text:
                if memory.last_location:
                    params["x"], params["y"], params["z"] = memory.last_location
            else:
                text_lower = text.lower()
                
                if any(kw in text_lower for kw in ["find", "search", "nearest", "nearby", "all"]):
                    for base_name, variants in structure_variants.items():
                        if base_name in text_lower or any(v.replace("_", " ") in text_lower or v.replace("_", "") in text_lower.replace(" ", "") for v in variants):
                            result = f"=== FINDING NEAREST {base_name.upper().replace('_', ' ')} ===\n\n"
                            if memory.last_location:
                                result += f"Your current position: {memory.last_location}\n\n"
                            
                            result += "Step 1 - Get your exact coords:\n"
                            result += "/execute in minecraft:overworld run query entity @s pos\n\n"
                            result += f"Step 2 - Run ALL these locate commands:\n"
                            for i, v in enumerate(variants, 1):
                                result += f"{i}. /locate {v}\n"
                            result += "\nStep 3 - Calculate distance for each result:\n"
                            result += "In chat, compare distances and pick the nearest.\n\n"
                            result += "Step 4 - Teleport to nearest:\n"
                            result += "/tp @s <x> <y> <z>"
                            return {"type": "command", "result": result}
                
                matched_structure = None
                for struct in structure_names:
                    if struct.replace("_", " ") in text_lower or struct.replace("_", "") in text_lower.replace(" ", ""):
                        matched_structure = struct
                        break
                if matched_structure:
                    return {"type": "command", "result": f"/locate {matched_structure}\nThen run: /tp @s <x> <y> <z>\n(Use the coordinates from the locate command)"}

        if command_name == "kill":
            text_lower = text.lower()
            mob_types = ["zombie", "skeleton", "creeper", "spider", "enderman", "pig", "cow", "sheep", "chicken", "horse", "donkey", "llama", "wolf", "cat", "parrot", "rabbit", "fox", "panda", "bee", "slime", "magma_cube", "blaze", "ghast", "piglin", "hoglin", "stray", "drowned", "husk", "pillager", "ravager", "vindicator", "evoker", "vex", "shulker", "guardian", "elder_guardian", "wither", "ender_dragon", "player", "item", "arrow", "xp_orb"]
            
            if "all" in text_lower or "everything" in text_lower:
                return {"type": "command", "result": "/kill @e"}
            
            for mob in mob_types:
                if mob in text_lower:
                    return {"type": "command", "result": f"/kill @e[type={mob}]"}
            
            player_match = re.search(r'(?:player )?(\w+)', original_text.split("kill")[-1])
            if player_match:
                return {"type": "command", "result": f"/kill {player_match.group(1)}"}
            
            return {"type": "command", "result": "/kill @e"}

        if command_name == "locate":
            text_lower = text.lower()
            
            typo_fixes = {"strongld": "stronghold", "stronghol": "stronghold", "mansion": "woodland_mansion", "monument": "ocean_monument", "outpost": "pillager_outpost", "pyramid": "desert_pyramid", "temple": "desert_pyramid"}
            for typo, correct in typo_fixes.items():
                if typo in text_lower:
                    text_lower = text_lower.replace(typo, correct)
            matched_structure = None
            for struct in structure_names:
                if struct.replace("_", " ") in text_lower or struct.replace("_", "") in text_lower.replace(" ", ""):
                    matched_structure = struct
                    break
            if matched_structure:
                params["structure"] = matched_structure
        
        if "name" in engine.commands.get(command_name, ""):
            words = original_text.split()
            if len(words) > 1:
                params["name"] = words[-1]

        command = engine.build(command_name, params)

        if command:
            command = command.replace("{player}", "@s")
            for key in ["{x}", "{y}", "{z}", "{item}", "{count}", "{structure}", "{name}", "{mode}", "{time}", "{weather}", "{effect}", "{enchantment}", "{amount}", "{block}", "{entity}", "{objective}", "{team}", "{value}", "{difficulty}"]:
                command = command.replace(key, "")
            command = re.sub(r'\s+', ' ', command).strip()
        
        return {"type": "command", "result": command}
    else:
        text_lower = text.lower()
        if "where am i" in text_lower or "my coordinates" in text_lower or "my position" in text_lower:
            result = "To find your coordinates in Minecraft:\n\n"
            result += "1. Press F3 (or Fn+F3 on laptops) to open Debug Screen\n"
            result += "2. Look for 'XYZ' section - shows your current position\n\n"
            result += "Or use this command:\n/execute in minecraft:overworld run query entity @s pos\n\n"
            result += "Your last known position from memory: "
            if memory.last_location:
                result += f"{memory.last_location}"
            else:
                result += "Unknown (run /tp or provide coordinates first)"
            memory.add_chat(text)
            return {"type": "chat", "result": result}
        
        from core.ai_chat import chat
        reply = chat(text, memory.chat_history)
        memory.add_chat(text)
        return {"type": "chat", "result": reply}
