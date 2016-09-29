%{?scl:%scl_package gmavenplus-plugin}
%{!?scl:%global pkg_name %{name}}

Name:          %{?scl_prefix}gmavenplus-plugin
Version:       1.5
Release:       2%{?dist}
Summary:       Integrates Groovy into Maven projects
License:       ASL 2.0
URL:           http://groovy.github.io/GMavenPlus/
Source0:       https://github.com/groovy/GMavenPlus/archive/%{version}.tar.gz

BuildRequires: maven-local
BuildRequires: %{?scl_mvn_prefix}jline
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.ant:ant)
BuildRequires: mvn(org.apache.ant:ant-antlr)
BuildRequires: mvn(org.apache.ant:ant-junit)
BuildRequires: mvn(org.apache.ant:ant-launcher)
BuildRequires: %{?scl_mvn_prefix}apache-ivy
BuildRequires: mvn(org.apache.maven:maven-core)
BuildRequires: mvn(org.apache.maven:maven-plugin-api)
BuildRequires: mvn(org.apache.maven:maven-plugin-registry)
BuildRequires: mvn(org.apache.maven:maven-project)
BuildRequires: mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-invoker-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires: mvn(org.apache.maven.shared:file-management)
BuildRequires: mvn(org.codehaus:codehaus-parent:pom:)
# Groovy only used in non-SCL package
%{!?scl:BuildRequires: mvn(org.codehaus.groovy:groovy-all)}
%{!?scl:BuildRequires: mvn(org.codehaus.groovy:groovy-ant)}
BuildRequires: mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires: mvn(org.codehaus.plexus:plexus-cli)
BuildRequires: mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires: mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires: %{?scl_java_prefix}jansi
BuildRequires: %{?scl_mvn_prefix}mockito
# IT tests deps are not used in SCL package
%{!?scl:BuildRequires: mvn(ch.qos.logback:logback-classic)}
%{!?scl:BuildRequires: mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)}
%{!?scl:BuildRequires: mvn(org.codehaus.plexus:plexus-utils)}
%{?scl:Requires: %scl_runtime}

BuildArch:     noarch

%description
GMavenPlus is a rewrite of GMaven, a Maven plugin
that allows you to integrate Groovy into your
Maven projects.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n GMavenPlus-%{version}

%{?scl_enable}
%pom_remove_plugin :maven-clean-plugin
%pom_remove_plugin :maven-dependency-plugin
%pom_remove_plugin :maven-help-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :cobertura-maven-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-deploy-plugin
%pom_remove_plugin :maven-site-plugin

%pom_xpath_remove "pom:build/pom:extensions"
%pom_xpath_remove "pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions"

# Mockito cannot mock this class: class org.codehaus.gmavenplus.mojo.AbstractGroovyMojoTest$TestGroovyMojo
rm -r src/test/java/org/codehaus/gmavenplus/mojo/AbstractGroovyMojoTest.java

# Convert from dos to unix line ending
sed -i.orig 's|\r||g' README.markdown
touch -r README.markdown.orig README.markdown
rm README.markdown.orig

# remove Groovy from SCL package
%{?scl:%pom_remove_dep org.codehaus.groovy:groovy-all}
%{?scl:%pom_remove_dep org.codehaus.groovy:groovy-ant}
%{?scl:rm -f src/test/java/org/codehaus/gmavenplus/mojo/AbstractToolsMojoTest.java} 
%{?scl:rm -f src/test/java/org/codehaus/gmavenplus/mojo/ExecuteMojoTest.java} 
%{?scl:rm -f src/test/java/org/codehaus/gmavenplus/mojo/GroovydocMojoTest.java} 
%{?scl:rm -f src/test/java/org/codehaus/gmavenplus/mojo/GroovydocTestsMojoTest.java} 

# lower JDK version in enforcer plugin for SCL package
%{?scl:%pom_xpath_set "pom:build/pom:plugins/pom:plugin/pom:executions/pom:execution/pom:configuration/pom:rules/pom:requireJavaVersion/pom:version" "[1.7,)"}

%mvn_file : %{pkg_name}
%{?scl_disable}

%build
%{?scl_enable}
%mvn_build -- -Pnonindy
%{?scl_disable}

%install
%{?scl_enable}
%mvn_install
%{?scl_disable}

%files -f .mfiles
%doc README.markdown
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Thu Sep 29 2016 Tomas Repik <trepik@redhat.com> - 1.5-2
- scl conversion

* Wed Apr 01 2015 gil cattaneo <puntogil@libero.it> 1.5-1
- initial rpm
