'use strict';
const path = require('path');
const fs = require('fs');

// Files that are used for CI scripts
// we want to make decisions based on these changing
const CI_FILES = [
  '.github/workflows/build-ci.yml',
  'tools/genmatrix.js',
  'tests/integration',
  'tests/integration_runner.py'
];

// Regular expression for detecting version numbering of Dogecoin Core
// used to detect which versions are what
const VERSION_DIR_RE = /^\d+\.\d+\.\d+$/;

// Entry in the matrix, resistant to red and blue pills
class MatrixEntry {
  constructor (version, variant, platform) {
    this.version = version;
    this.variant = variant;
    this.platform = platform;
  }

  // returns the relative path to the version/variant as string
  path () {
    return path.join(this.version, this.variant);
  }

  // prints the entry to console
  print () {
    console.log(this.version, this.variant, this.platform);
  }
}

// Build a GH Actions matrix
class MatrixBuilder {
  constructor (baseDir) {
    this.baseDir = baseDir;
    this.matrix = [];
  }

  // read a build matrix from the repository's directory hieararchy
  readMatrix () {
    // [1] read the versions from the repository root
    const versions = this.readAllVersions();
    if (!Array.isArray(versions) || versions.length < 1) {
      throw new Error('No versions to iterate');
    }

    // iterate all versions
    versions.forEach(version => {
      // [2] read the variants from the version directory
      const variants = this.readVariantsForVersion(version);
      if (!Array.isArray(variants) || variants.length < 1) {
        throw new Error('No variants to iterate for ' + version);
      }

      // iterate each variant for this version
      variants.forEach(variant => {
        // [3] Read the target platforms for this version/variant combination
        const platforms = this.readPlatformsForVersionVariant(version, variant);
        if (!Array.isArray(platforms) || platforms.length < 1) {
          throw new Error('No platforms to iterate for ' + path.join(version, variant));
        }

        platforms.forEach(platform => {
          // [4] Add an entry to the matrix for each version/variant/platform
          //     combination
          this.matrix.push(new MatrixEntry(version, variant, platform));
        });
      });
    });
  }

  // read all subdirectories inside a given directory
  // returns array of DirEnt objects
  readDirs (fromDir) {
    const files = fs.readdirSync(fromDir, { withFileTypes: true });
    return files.filter(file => file.isDirectory());
  }

  // read all the version directories in the builder's baseDir
  // returns array of filename strings
  readAllVersions () {
    const dirs = this.readDirs(this.baseDir);
    const versionDirs = dirs.filter(dir => dir.name.match(VERSION_DIR_RE));
    return versionDirs.map(dir => dir.name);
  }

  // read all variants for a specific version
  // returns array of filename strings
  readVariantsForVersion (version) {
    const fromDir = path.resolve(this.baseDir, version);
    const dirs = this.readDirs(fromDir);
    return dirs.map(dir => dir.name);
  }

  // read all platforms for a specific version
  // returns array of architecture strings, eg ["linux/amd64", "linux/arm64"]
  readPlatformsForVersionVariant (version, variant) {
    const pathToPlatformFile = path.resolve(this.baseDir, version, variant, 'PLATFORMS');

    if (!fs.existsSync(pathToPlatformFile)) {
      throw new Error('No PLATFORM file for ' + path.join(version, variant));
    }

    const contents = fs.readFileSync(pathToPlatformFile).toString('utf-8');
    const platforms = contents.split('\n');

    return platforms
      .map(platform => platform.trim()) // remove whitespace just in case
      .filter(platform => platform !== ''); // remove empty string entries
  }

  // filters the matrix against an array of files
  filterIncludedVariants (fileList) {
    this.matrix = this.matrix.filter(entry => {
      const matchRegex = new RegExp(entry.path());
      return fileList.some(file => file.match(matchRegex));
    });
  }

  // output the expected GH Actions format
  build () {
    return this.matrix.length > 0 ? { include: this.matrix } : null;
  }
}

// Checks if any of the CI files have been changed
const checkCIFilesChanged = (changedFiles) => {
  return CI_FILES.some(file => changedFiles.some(changedFile => {
    return changedFile.match(new RegExp(file));
  }));
};

const generateMatrix = (baseDir, changedFiles) => {
  const builder = new MatrixBuilder(baseDir);

  // populate the matrix with all builds
  builder.readMatrix();

  // If the CI has changed, test all builds, otherwise, just build what's changed
  if (checkCIFilesChanged(changedFiles)) {
    console.log('CI files have changed, running all builds!');
  } else {
    builder.filterIncludedVariants(changedFiles);
  }

  // print the build list for auditability.
  console.log('BUILD LIST:');
  builder.matrix.forEach(entry => entry.print());

  // return the GH Actions expected matrix format as { "include": [Object] }
  // or null if there are no entries
  return builder.build();
};

module.exports = generateMatrix;
