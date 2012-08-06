#!/usr/bin/env python
#
# Copyright (c) 2012 Patroklos Argyroudis <argp at domain census-labs.com>
# Copyright (c) 2012 Chariton Karamitas <huku at domain census-labs.com>
# Copyright (c) 2012 Census, Inc. (http://www.census-labs.com/)

import sys
import os

def usage(name):
    print '[*] usage: %s <firefox app directory>' % (name)
    return

def handle_dir(args, dirname, filenames):
    # print '[+] directory %s' % (dirname)
    
    for filename in filenames:
        pathname = '%s/%s' % (dirname, filename)
        ext = os.path.splitext(pathname)[1]

        # check if we have debugging symbols for this binary
        # if we have, let's fix it so that gdb 7.x can load it
        if ext == '.dSYM':
            print '[+] pathname %s' % (pathname)
            # print '[+] filename %s' % (filename)
            
            orig_pathname = pathname.replace('.dSYM', '.orig')
            x86_64_pathname = pathname.replace('.dSYM', '.x86_64')
            old_pathname = pathname.replace('.dSYM', '')

            print '     [+] orig_pathname: %s' % (orig_pathname)
            print '     [+] x86_64_pathname: %s' % (x86_64_pathname)
            print '     [+] old_pathname: %s' % (old_pathname)
        
            # first fix the binary itself
            if os.path.exists(orig_pathname) and os.path.exists(x86_64_pathname):
                print '     [+] binary already done: %s\n' % (old_pathname)
            else:
                os.system('cp -f %s %s' % (old_pathname, orig_pathname))
                os.system('lipo -thin x86_64 %s -o %s' % (old_pathname, x86_64_pathname))
                os.system('cp -f %s %s' % (x86_64_pathname, old_pathname))

                print '     [+] binary fixed: %s\n' % (old_pathname)

            # now let's handle the binary's corresponding DWARF file
            dwarf_pathname = '%s/Contents/Resources/DWARF/%s' % (pathname, filename.replace('.dSYM', ''))
            print '     [+] dwarf_pathname: %s' % (dwarf_pathname)

            orig_dwarf_pathname = '%s.orig' % (dwarf_pathname)
            x86_64_dwarf_pathname = '%s.x86_64' % (dwarf_pathname)

            print '     [+] orig_dwarf_pathname: %s' % (orig_dwarf_pathname)
            print '     [+] x86_64_dwarf_pathname: %s' % (x86_64_dwarf_pathname)

            if os.path.exists(orig_dwarf_pathname) and os.path.exists(x86_64_dwarf_pathname):
                print '     [+] dwarf binary already done: %s\n' % (dwarf_pathname)
            else:
                os.system('cp -f %s %s' % (dwarf_pathname, orig_dwarf_pathname))
                os.system('lipo -thin x86_64 %s -o %s' % (dwarf_pathname, x86_64_dwarf_pathname))
                os.system('cp -f %s %s' % (x86_64_dwarf_pathname, dwarf_pathname))

                print '     [+] dwarf binary fixed: %s\n' % (dwarf_pathname)

def main(argv):
    argc = len(argv)

    if argc != 2:
        usage(argv[0])
        sys.exit(0)

    if os.path.isdir(argv[1]):
        firefox_dir = argv[1]
    else:
        print '[!] error: directory \'%s\' doesn\'t exist' % (argv[1])
        sys.exit(1)

    os.path.walk(firefox_dir, handle_dir, None)
 
if __name__ == '__main__':
    main(sys.argv)
    sys.exit(0)

# EOF
