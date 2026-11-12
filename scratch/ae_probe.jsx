
try {
    var f = new File('V:/___VAC/__K/__CODE/_PLUG_SCRIPT/vac34_ae_plugs/scratch/ae_test_output.txt');
    f.open('w');
    f.writeln('AE_APP_NAME=' + app.name);
    f.writeln('AE_APP_VERSION=' + app.version);
    f.writeln('AE_APP_ISWATCHFOLDER=' + app.isWatchFolder);
    f.writeln('AE_APP_PROJECT=' + (app.project ? app.project.file : 'none'));
    f.close();
} catch(e) {
    var f2 = new File('V:/___VAC/__K/__CODE/_PLUG_SCRIPT/vac34_ae_plugs/scratch/ae_test_output.txt');
    f2.open('w');
    f2.writeln('ERROR=' + e.toString());
    f2.close();
}
