namespace :entypo do
    task :compile do
        puts "Compiling icons..."
        puts %x(fontcustom compile)
    end
end

task :default => 'entypo:compile'

task :clean do
    puts "Removing generated fonts / css / testing site from _static/"
    FileUtils.rm_rf(Dir.glob('_static/*'))
    puts "Deleting fontcustom manifest"
    FileUtils.rm_rf(".fontcustom-manifest.json")
end
