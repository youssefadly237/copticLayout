# Coptic Layout

1. create dirs you need

   ```bash
   mkdir -p ~/.config/xkb/symbols
   mkdir -p ~/.config/xkb/rules
   ```

2. put your generated symbols file there

   ```bash
   python3 main.py
   cp Egyptian.xkb ~/.config/xkb/symbols/egyptian
   ```

3. create `~/.config/xkb/rules/evdev.xml`

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE xkbConfigRegistry SYSTEM "xkb.dtd">
   <xkbConfigRegistry version="1.1">
     <layoutList>
       <layout>
         <configItem>
           <name>egyptian</name>
           <shortDescription>cop</shortDescription>
           <description>Coptic (Egyptian)</description>
           <languageList>
             <iso639Id>cop</iso639Id>
           </languageList>
         </configItem>
       </layout>
     </layoutList>
   </xkbConfigRegistry>
   ```

4. verify it exits

```bash
xkbcli list | grep -i egyptian
```
