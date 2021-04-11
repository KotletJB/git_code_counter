#!/usr/bin/env python3

import os
import subprocess
import re 
import pandas as pd
import fire

list_of_suffixs = ('.abap', '.asc', '.ash', '.ampl', '.mod', '.g4', '.apib', '.apl', '.dyalog', '.asp', '.asax', '.ascx', '.ashx', '.asmx', '.aspx', '.axd', '.dats', '.hats', '.sats', '.as', '.adb', '.ada', '.ads', '.agda', '.als', '.apacheconf', '.vhost', '.cls', '.applescript', '.scpt', '.arc', '.ino', '.asciidoc', '.adoc', '.asc', '.aj', '.asm', '.a51', '.inc', '.nasm', '.aug', '.ahk', '.ahkl', '.au3', '.awk', '.auk', '.gawk', '.mawk', '.nawk', '.bat', '.cmd', '.befunge', '.bison', '.bb', '.bb', '.decls', '.bmx', '.bsv', '.boo', '.b', '.bf', '.brs', '.bro', '.c', '.cats', '.h', '.idc', '.w', '.cs', '.cake', '.cshtml', '.csx', '.cpp', '.c++', '.cc', '.cp', '.cxx', '.h', '.h++', '.hh', '.hpp', '.hxx', '.inc', '.inl', '.ipp', '.tcc', '.tpp', '.c-objdump', '.chs', '.clp', '.cmake', '.cmake.in', '.cob', '.cbl', '.ccp', '.cobol', '.cpy', '.css', '.csv', '.capnp', '.mss', '.ceylon', '.chpl', '.ch', '.ck', '.cirru', '.clw', '.icl', '.dcl', '.click', '.clj', '.boot', '.cl2', '.cljc', '.cljs', '.cljs.hl', '.cljscm', '.cljx', '.hic', '.coffee', '._coffee', '.cake', '.cjsx', '.cson', '.iced', '.cfm', '.cfml', '.cfc', '.lisp', '.asd', '.cl', '.l', '.lsp', '.ny', '.podsl', '.sexp', '.cp', '.cps', '.cl', '.coq', '.v', '.cppobjdump', '.c++-objdump', '.c++objdump', '.cpp-objdump', '.cxx-objdump', '.creole', '.cr', '.feature', '.cu', '.cuh', '.cy', '.pyx', '.pxd', '.pxi', '.d', '.di', '.d-objdump', '.com', '.dm', '.zone', '.arpa', '.d', '.darcspatch', '.dpatch', '.dart', '.diff', '.patch', '.dockerfile', '.djs', '.dylan', '.dyl', '.intr', '.lid', '.E', '.ecl', '.eclxml', '.ecl', '.sch', '.brd', '.epj', '.e', '.ex', '.exs', '.elm', '.el', '.emacs', '.emacs.desktop', '.em', '.emberscript', '.erl', '.es', '.escript', '.hrl', '.xrl', '.yrl', '.fs', '.fsi', '.fsx', '.fx', '.flux', '.f90', '.f', '.f03', '.f08', '.f77', '.f95', '.for', '.fpp', '.factor', '.fy', '.fancypack', '.fan', '.fs', '.for', '.eam.fs', '.fth', '.4th', '.f', '.for', '.forth', '.fr', '.frt', '.fs', '.ftl', '.fr', '.g', '.gco', '.gcode', '.gms', '.g', '.gap', '.gd', '.gi', '.tst', '.s', '.ms', '.gd', '.glsl', '.fp', '.frag', '.frg', '.fs', '.fsh', '.fshader', '.geo', '.geom', '.glslv', '.gshader', '.shader', '.vert', '.vrx', '.vsh', '.vshader', '.gml', '.kid', '.ebuild', '.eclass', '.po', '.pot', '.glf', '.gp', '.gnu', '.gnuplot', '.plot', '.plt', '.go', '.golo', '.gs', '.gst', '.gsx', '.vark', '.grace', '.gradle', '.gf', '.gml', '.graphql', '.dot', '.gv', '.man', '.1', '.1in', '.1m', '.1x', '.2', '.3', '.3in', '.3m', '.3qt', '.3x', '.4', '.5', '.6', '.7', '.8', '.9', '.l', '.me', '.ms', '.n', '.rno', '.roff', '.groovy', '.grt', '.gtpl', '.gvy', '.gsp', '.hcl', '.tf', '.hlsl', '.fx', '.fxh', '.hlsli', '.html', '.htm', '.html.hl', '.inc', '.st', '.xht', '.xhtml', '.mustache', '.jinja', '.eex', '.erb', '.erb.deface', '.phtml', '.http', '.hh', '.php', '.haml', '.haml.deface', '.handlebars', '.hbs', '.hb', '.hs', '.hsc', '.hx', '.hxsl', '.hy', '.bf', '.pro', '.dlm', '.ipf', '.ini', '.cfg', '.prefs', '.pro', '.properties', '.irclog', '.weechatlog', '.idr', '.lidr', '.ni', '.i7x', '.iss', '.io', '.ik', '.thy', '.ijs', '.flex', '.jflex', '.json', '.geojson', '.lock', '.topojson', '.json5', '.jsonld', '.jq', '.jsx', '.jade', '.j', '.java', '.jsp', '.js', '._js', '.bones', '.es', '.es6', '.frag', '.gs', '.jake', '.jsb', '.jscad', '.jsfl', '.jsm', '.jss', '.njs', '.pac', '.sjs', '.ssjs', '.sublime-build', '.sublime-commands', '.sublime-completions', '.sublime-keymap', '.sublime-macro', '.sublime-menu', '.sublime-mousemap', '.sublime-project', '.sublime-settings', '.sublime-theme', '.sublime-workspace', '.sublime_metrics', '.sublime_session', '.xsjs', '.xsjslib', '.jl', '.ipynb', '.krl', '.sch', '.brd', '.kicad_pcb', '.kit', '.kt', '.ktm', '.kts', '.lfe', '.ll', '.lol', '.lsl', '.lslp', '.lvproj', '.lasso', '.las', '.lasso8', '.lasso9', '.ldml', '.latte', '.lean', '.hlean', '.less', '.l', '.lex', '.ly', '.ily', '.b', '.m', '.ld', '.lds', '.mod', '.liquid', '.lagda', '.litcoffee', '.lhs', '.ls', '._ls', '.xm', '.x', '.xi', '.lgt', '.logtalk', '.lookml', '.ls', '.lua', '.fcgi', '.nse', '.pd_lua', '.rbxs', '.wlua', '.mumps', '.m', '.m4', '.m4', '.ms', '.mcr', '.mtml', '.muf', '.m', '.mak', '.d', '.mk', '.mkfile', '.mako', '.mao', '.md', '.markdown', '.mkd', '.mkdn', '.mkdown', '.ron', '.mask', '.mathematica', '.cdf', '.m', '.ma', '.mt', '.nb', '.nbp', '.wl', '.wlt', '.matlab', '.m', '.maxpat', '.maxhelp', '.maxproj', '.mxt', '.pat', '.mediawiki', '.wiki', '.m', '.moo', '.metal', '.minid', '.druby', '.duby', '.mir', '.mirah', '.mo', '.mod', '.mms', '.mmk', '.monkey', '.moo', '.moon', '.myt', '.ncl', '.nl', '.nsi', '.nsh', '.n', '.axs', '.axi', '.axs.erb', '.axi.erb', '.nlogo', '.nl', '.lisp', '.lsp', '.nginxconf', '.vhost', '.nim', '.nimrod', '.ninja', '.nit', '.nix', '.nu', '.numpy', '.numpyw', '.numsc', '.ml', '.eliom', '.eliomi', '.ml4', '.mli', '.mll', '.mly', '.objdump', '.m', '.h', '.mm', '.j', '.sj', '.omgrofl', '.opa', '.opal', '.cl', '.opencl', '.p', '.cls', '.scad', '.org', '.ox', '.oxh', '.oxo', '.oxygene', '.oz', '.pwn', '.inc', '.php', '.aw', '.ctp', '.fcgi', '.inc', '.php3', '.php4', '.php5', '.phps', '.phpt', '.pls', '.pck', '.pkb', '.pks', '.plb', '.plsql', '.sql', '.sql', '.pov', '.inc', '.pan', '.psc', '.parrot', '.pasm', '.pir', '.pas', '.dfm', '.dpr', '.inc', '.lpr', '.pp', '.pl', '.al', '.cgi', '.fcgi', '.perl', '.ph', '.plx', '.pm', '.pod', '.psgi', '.t', '.6pl', '.6pm', '.nqp', '.p6', '.p6l', '.p6m', '.pl', '.pl6', '.pm', '.pm6', '.t', '.pkl', '.l', '.pig', '.pike', '.pmod', '.pod', '.pogo', '.pony', '.ps', '.eps', '.ps1', '.psd1', '.psm1', '.pde', '.pl', '.pro', '.prolog', '.yap', '.spin', '.proto', '.asc', '.pub', '.pp', '.pd', '.pb', '.pbi', '.purs', '.py', '.bzl', '.cgi', '.fcgi', '.gyp', '.lmi', '.pyde', '.pyp', '.pyt', '.pyw', '.rpy', '.tac', '.wsgi', '.xpy', '.pytb', '.qml', '.qbs', '.pro', '.pri', '.r', '.rd', '.rsx', '.raml', '.rdoc', '.rbbas', '.rbfrm', '.rbmnu', '.rbres', '.rbtbar', '.rbuistate', '.rhtml', '.rmd', '.rkt', '.rktd', '.rktl', '.scrbl', '.rl', '.raw', '.reb', '.r', '.r2', '.r3', '.rebol', '.red', '.reds', '.cw', '.rpy', '.rs', '.rsh', '.robot', '.rg', '.rb', '.builder', '.fcgi', '.gemspec', '.god', '.irbrc', '.jbuilder', '.mspec', '.pluginspec', '.podspec', '.rabl', '.rake', '.rbuild', '.rbw', '.rbx', '.ru', '.ruby', '.thor', '.watchr', '.rs', '.rs.in', '.sas', '.scss', '.smt2', '.smt', '.sparql', '.rq', '.sqf', '.hqf', '.sql', '.cql', '.ddl', '.inc', '.prc', '.tab', '.udf', '.viw', '.sql', '.db2', '.ston', '.svg', '.sage', '.sagews', '.sls', '.sass', '.scala', '.sbt', '.sc', '.scaml', '.scm', '.sld', '.sls', '.sps', '.ss', '.sci', '.sce', '.tst', '.self', '.sh', '.bash', '.bats', '.cgi', '.command', '.fcgi', '.ksh', '.sh.in', '.tmux', '.tool', '.zsh', '.sh-session', '.shen', '.sl', '.slim', '.smali', '.st', '.cs', '.tpl', '.sp', '.inc', '.sma', '.nut', '.stan', '.ML', '.fun', '.sig', '.sml', '.do', '.ado', '.doh', '.ihlp', '.mata', '.matah', '.sthlp', '.styl', '.sc', '.scd', '.swift', '.sv', '.svh', '.vh', '.toml', '.txl', '.tcl', '.adp', '.tm', '.tcsh', '.csh', '.tex', '.aux', '.bbx', '.bib', '.cbx', '.cls', '.dtx', '.ins', '.lbx', '.ltx', '.mkii', '.mkiv', '.mkvi', '.sty', '.toc', '.tea', '.t', '.txt', '.fr', '.nb', '.ncl', '.no', '.textile', '.thrift', '.t', '.tu', '.ttl', '.twig', '.ts', '.tsx', '.upc', '.anim', '.asset', '.mat', '.meta', '.prefab', '.unity', '.uno', '.uc', '.ur', '.urs', '.vcl', '.vhdl', '.vhd', '.vhf', '.vhi', '.vho', '.vhs', '.vht', '.vhw', '.vala', '.vapi', '.v', '.veo', '.vim', '.vb', '.bas', '.cls', '.frm', '.frx', '.vba', '.vbhtml', '.vbs', '.volt', '.vue', '.owl', '.webidl', '.x10', '.xc', '.xml', '.ant', '.axml', '.ccxml', '.clixml', '.cproject', '.csl', '.csproj', '.ct', '.dita', '.ditamap', '.ditaval', '.dll.config', '.dotsettings', '.filters', '.fsproj', '.fxml', '.glade', '.gml', '.grxml', '.iml', '.ivy', '.jelly', '.jsproj', '.kml', '.launch', '.mdpolicy', '.mm', '.mod', '.mxml', '.nproj', '.nuspec', '.odd', '.osm', '.plist', '.pluginspec', '.props', '.ps1xml', '.psc1', '.pt', '.rdf', '.rss', '.scxml', '.srdf', '.storyboard', '.stTheme', '.sublime-snippet', '.targets', '.tmCommand', '.tml', '.tmLanguage', '.tmPreferences', '.tmSnippet', '.tmTheme', '.ts', '.tsx', '.ui', '.urdf', '.ux', '.vbproj', '.vcxproj', '.vssettings', '.vxml', '.wsdl', '.wsf', '.wxi', '.wxl', '.wxs', '.x3d', '.xacro', '.xaml', '.xib', '.xlf', '.xliff', '.xmi', '.xml.dist', '.xproj', '.xsd', '.xul', '.zcml', '.xsp-config', '.xsp.metadata', '.xpl', '.xproc', '.xquery', '.xq', '.xql', '.xqm', '.xqy', '.xs', '.xslt', '.xsl', '.xojo_code', '.xojo_menu', '.xojo_report', '.xojo_script', '.xojo_toolbar', '.xojo_window', '.xtend', '.yml', '.reek', '.rviz', '.sublime-syntax', '.syntax', '.yaml', '.yaml-tmlanguage', '.yang', '.y', '.yacc', '.yy', '.zep', '.zimpl', '.zmpl', '.zpl', '.desktop', '.desktop.in', '.ec', '.eh', '.edn', '.fish', '.mu', '.nc', '.ooc', '.rst', '.rest', '.rest.txt', '.rst.txt', '.wisp', '.prg', '.ch', '.prw')
list_of_links_to_repos = ['https://github.com/KotletJB/file_observer.git','https://github.com/mx0c/super-mario-python.git']


def counter(list_of_links_to_repos = list_of_links_to_repos):
    if type(list_of_links_to_repos) != type(list()):
        with open(list_of_links_to_repos) as f:
            list_of_links_to_repos = [x.strip() for x in f.readlines()]
    Words_dict = {}
    Lines = 0
    Signs = 0
    Words = 0

    for repo in list_of_links_to_repos:
        try:
            name_of_repo = re.findall('/([0-9A-Za-z_-]+)\.git',repo)[0]
            subprocess.run(['git', 'clone', repo])

            thisdir = os.getcwd() + '/' + name_of_repo
            # r=root, d=directories, f = files
            for r, d, f in os.walk(thisdir):
                for file in f:
                    if file.endswith(list_of_suffixs):
                        fille = os.path.join(r, file)
                        with open(fille) as fp:
                            list_of_lines = fp.readlines()
                            Lines += len(list_of_lines)

                            for line in list_of_lines:
                                Signs += len(line)
                                lin = line.strip().split()
                                Words += len(lin)
                                for word in lin:
                                    if word not in Words_dict:
                                        Words_dict[word] = 1
                                    else:
                                        Words_dict[word] += 1

            subprocess.run(['rm', '-rf', name_of_repo])
        except:
            pass
    print('\nTotal:')
    print('Lines:',Lines)
    print('Words:',Words)
    print('Signs:',Signs)
    sort_dic = dict(sorted(Words_dict.items(), key= lambda item: item[1], reverse=True))
    data = pd.DataFrame(sort_dic.items(), columns=['word','count'])
    print(data.head(10))
    

if __name__ == "__main__":
    fire.Fire(counter)
