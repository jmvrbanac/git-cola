from PyQt4 import QtCore
from PyQt4 import QtGui

from cola import qtutils
from cola.views import log
from cola.qtutils import tr
from cola.views.standard import create_standard_widget

MainWindowBase = create_standard_widget(QtGui.QMainWindow)
class MainWindow(MainWindowBase):
    def __init__(self, parent=None):
        MainWindowBase.__init__(self, parent)
        # Default size; this is thrown out when save/restore is used
        self.resize(888, 420)
        self.setDockOptions(QtGui.QMainWindow.AllowNestedDocks |
                            QtGui.QMainWindow.AllowTabbedDocks |
                            QtGui.QMainWindow.AnimatedDocks)

        # Create the application menu
        self.menubar = QtGui.QMenuBar(self)
        self.edit_menu = self.create_menu('Edit', self.menubar)
        self.file_menu = self.create_menu('File', self.menubar)
        self.merge_menu = self.create_menu('Merge', self.menubar)
        self.help_menu = self.create_menu('Help', self.menubar)
        self.diff_menu = self.create_menu('Diff', self.menubar)
        self.menu_tools = self.create_menu('Tools', self.menubar)

        self.commit_menu = self.create_menu('Commit', self.menubar)
        self.menu_show = self.create_menu('View', self.commit_menu)
        self.menu_prepare = self.create_menu('Prepare', self.commit_menu)
        self.menu_advanced = self.create_menu('Advanced', self.commit_menu)

        self.search_menu = self.create_menu('Search', self.menubar)
        self.menu_search_more = self.create_menu('More...', self.search_menu)

        self.branch_menu = self.create_menu('Branch', self.menubar)
        self.menu_branch_view = self.create_menu('View', self.branch_menu)
        self.menu_branch_advanced = self.create_menu('Advanced', self.branch_menu)

        self.setMenuBar(self.menubar)

        # "Actions" widget
        self.actiondockwidget = self.create_dock('Actions')
        self.actiondockwidgetcontents = QtGui.QWidget()
        self.actiondockwidgetlayout = QtGui.QVBoxLayout(self.actiondockwidgetcontents)
        self.actiondockwidgetlayout.setSpacing(3)
        self.actiondockwidgetlayout.setMargin(3)

        self.rescan_button = self.create_button('Rescan', self.actiondockwidgetcontents)
        self.stage_button = self.create_button('Stage Changed', self.actiondockwidgetcontents)
        self.signoff_button = self.create_button('Sign Off', self.actiondockwidgetcontents)
        self.commit_button = self.create_button('Commit@@verb', self.actiondockwidgetcontents)
        self.fetch_button = self.create_button('Fetch', self.actiondockwidgetcontents)
        self.push_button = self.create_button('Push', self.actiondockwidgetcontents)
        self.pull_button = self.create_button('Pull', self.actiondockwidgetcontents)
        self.stash_button = self.create_button('Stash', self.actiondockwidgetcontents)
        self.alt_button = self.create_button('...', self.actiondockwidgetcontents)
        self.alt_button.hide()

        self.column_label = QtGui.QLabel(self.actiondockwidgetcontents)
        self.column_label.setAlignment(QtCore.Qt.AlignCenter)
        self.actiondockwidgetlayout.addWidget(self.column_label)

        self.action_spacer = QtGui.QSpacerItem(1, 1,
                                               QtGui.QSizePolicy.Minimum,
                                               QtGui.QSizePolicy.MinimumExpanding)
        self.actiondockwidgetlayout.addItem(self.action_spacer)
        self.actiondockwidget.setWidget(self.actiondockwidgetcontents)

        # "Repository Status" widget
        self.statusdockwidget = self.create_dock('Repository Status')
        self.statusdockwidgetcontents = QtGui.QWidget()
        self.statusdockwidgetlayout = QtGui.QVBoxLayout(self.statusdockwidgetcontents)
        self.statusdockwidgetlayout.setMargin(3)

        self.status_tree = QtGui.QTreeWidget(self.statusdockwidgetcontents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_tree.sizePolicy().hasHeightForWidth())

        self.status_tree.setSizePolicy(sizePolicy)
        self.status_tree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.status_tree.setAnimated(True)
        self.status_tree.setHeaderHidden(True)

        item = QtGui.QTreeWidgetItem(self.status_tree)
        item = QtGui.QTreeWidgetItem(self.status_tree)
        item = QtGui.QTreeWidgetItem(self.status_tree)
        item = QtGui.QTreeWidgetItem(self.status_tree)

        self.statusdockwidgetlayout.addWidget(self.status_tree)
        self.statusdockwidget.setWidget(self.statusdockwidgetcontents)

        # "Commit Message Editor" widget
        self.commitdockwidget = self.create_dock('Commit Message Editor')
        self.commitdockwidgetcontents = QtGui.QWidget()

        self.commitdockwidgetlayout = QtGui.QVBoxLayout(self.commitdockwidgetcontents)
        self.commitdockwidgetlayout.setMargin(3)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setSpacing(0)

        self.commitmsg = QtGui.QTextEdit(self.commitdockwidgetcontents)
        self.commitmsg.setMinimumSize(QtCore.QSize(1, 1))
        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
                                   QtGui.QSizePolicy.Minimum)
        self.commitmsg.setSizePolicy(policy)
        self.commitmsg.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.commitmsg.setAcceptRichText(False)
        self.vboxlayout.addWidget(self.commitmsg)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(0)
        self.hboxlayout.setContentsMargins(0, -1, -1, -1)

        self.spacer = QtGui.QSpacerItem(1, 1,
                                        QtGui.QSizePolicy.Minimum,
                                        QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(self.spacer)

        self.new_commit_radio = QtGui.QRadioButton(self.commitdockwidgetcontents)
        self.new_commit_radio.setText(tr("New Commit"))
        self.hboxlayout.addWidget(self.new_commit_radio)

        self.amend_radio = QtGui.QRadioButton(self.commitdockwidgetcontents)
        self.amend_radio.setText(tr("Amend Last Commit"))
        self.hboxlayout.addWidget(self.amend_radio)

        self.vboxlayout.addLayout(self.hboxlayout)
        self.commitdockwidgetlayout.addLayout(self.vboxlayout)
        self.commitdockwidget.setWidget(self.commitdockwidgetcontents)

        # "Command Output" widget
        self.logdockwidget = self.create_dock('Command Output')
        self.logdockwidget.setWidget(qtutils.logger())

        # "Diff Viewer" widget
        self.diffdockwidget = self.create_dock('Diff Viewer')
        self.diffdockwidgetcontents = QtGui.QWidget()
        self.diffdockwidgetlayout = QtGui.QVBoxLayout(self.diffdockwidgetcontents)
        self.diffdockwidgetlayout.setMargin(3)

        self.display_text = QtGui.QTextEdit(self.diffdockwidgetcontents)
        self.display_text.setMinimumSize(QtCore.QSize(1, 1))
        self.display_text.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.display_text.setReadOnly(True)
        self.display_text.setAcceptRichText(False)
        self.display_text.setCursorWidth(2)
        self.display_text.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)

        self.diffdockwidgetlayout.addWidget(self.display_text)
        self.diffdockwidget.setWidget(self.diffdockwidgetcontents)

        self.menu_unstage_selected = self.create_action('Unstage From Commit')
        self.menu_show_diffstat = self.create_action('Diffstat')
        self.menu_show_index = self.create_action('Index')
        self.menu_stage_modified = self.create_action('Stage Changed Files To Commit')
        self.menu_stage_untracked = self.create_action('Stage All Untracked')
        self.menu_stage_selected = self.create_action('Stage Selected')
        self.menu_export_patches = self.create_action('Export Patches...')
        self.menu_cut = self.create_action('Cut')
        self.menu_copy = self.create_action('Copy')
        self.menu_paste = self.create_action('Paste')
        self.menu_select_all = self.create_action('Select All')
        self.menu_options = self.create_action('Options')
        self.menu_delete = self.create_action('Delete')
        self.menu_undo = self.create_action('Undo')
        self.menu_redo = self.create_action('Redo')
        self.menu_rescan = self.create_action('Rescan')
        self.menu_get_prev_commitmsg = self.create_action('Get Latest Commit Message')
        self.menu_cherry_pick = self.create_action('Cherry-Pick...')
        self.menu_unstage_all = self.create_action('Unstage All')
        self.menu_quit = self.create_action('Quit')
        self.menu_load_commitmsg = self.create_action('Load Commit Message...')
        self.menu_create_branch = self.create_action('Create...')
        self.menu_checkout_branch = self.create_action('Checkout...')
        self.menu_rebase_branch = self.create_action('Rebase...')
        self.menu_delete_branch = self.create_action('Delete...')

        self.menu_search_revision = self.create_action('Revision ID...')
        self.menu_search_path = self.create_action('Commits Touching Path(s)...')
        self.menu_search_revision_range = self.create_action('Revision Range...')
        self.menu_search_date_range = self.create_action('Latest Commits...')
        self.menu_search_message = self.create_action('Commit Messages...')
        self.menu_search_diff = self.create_action('Content Introduced in Commit...')
        self.menu_search_author = self.create_action('Commits By Author...')
        self.menu_search_committer = self.create_action('Commits By Committer...')

        self.menu_manage_bookmarks = self.create_action('Bookmarks...')
        self.menu_save_bookmark = self.create_action('Bookmark Current...')
        self.menu_search_grep = self.create_action('Grep')
        self.menu_merge_local = self.create_action('Local Merge...')
        self.menu_merge_abort = self.create_action('Abort Merge...')
        self.menu_open_repo = self.create_action('Open...')
        self.menu_stash = self.create_action('Stash...')

        self.menu_diff_branch = self.create_action('Apply Changes From...')
        self.menu_branch_compare = self.create_action('Branches...')
        self.menu_clone_repo = self.create_action('Clone...')
        self.menu_help_docs = self.create_action('Documentation')
        self.menu_commit_compare = self.create_action('Commits...')
        self.menu_visualize_current = self.create_action('Visualize Current Branch...')
        self.menu_visualize_all = self.create_action('Visualize All Branches...')
        self.menu_browse_commits = self.create_action('Commits...')
        self.menu_browse_branch = self.create_action('Browse Current Branch...')
        self.menu_browse_other_branch = self.create_action('Browse Other Branch...')
        self.menu_load_commitmsg_template = self.create_action('Get Commit Message Template')
        self.menu_commit_compare_file = self.create_action('Commits Touching File...')
        self.menu_help_about = self.create_action('About')
        self.menu_branch_diff = self.create_action('SHA-1...')
        self.menu_branch_review = self.create_action('Review...')
        self.menu_diff_expression = self.create_action('Expression...')
        self.menu_tools_classic = self.create_action('Cola Classic...')

        self.menu_show.addAction(self.menu_browse_commits)
        self.menu_show.addAction(self.menu_show_index)
        self.menu_show.addAction(self.menu_show_diffstat)
        
        self.menu_prepare.addAction(self.menu_stage_modified)
        self.menu_prepare.addAction(self.menu_stage_untracked)
        self.menu_prepare.addAction(self.menu_stage_selected)
        self.menu_prepare.addSeparator()
        self.menu_prepare.addAction(self.menu_unstage_all)
        self.menu_prepare.addAction(self.menu_unstage_selected)

        self.menu_advanced.addAction(self.menu_cherry_pick)

        self.commit_menu.addAction(self.menu_show.menuAction())
        self.commit_menu.addAction(self.menu_prepare.menuAction())
        self.commit_menu.addSeparator()
        self.commit_menu.addAction(self.menu_stash)
        self.commit_menu.addAction(self.menu_export_patches)
        self.commit_menu.addSeparator()
        self.commit_menu.addAction(self.menu_advanced.menuAction())

        self.edit_menu.addAction(self.menu_undo)
        self.edit_menu.addAction(self.menu_redo)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.menu_cut)
        self.edit_menu.addAction(self.menu_copy)
        self.edit_menu.addAction(self.menu_paste)
        self.edit_menu.addAction(self.menu_delete)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.menu_select_all)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.menu_options)

        self.menu_search_more.addAction(self.menu_search_author)
        self.menu_search_more.addAction(self.menu_search_path)
        self.menu_search_more.addAction(self.menu_search_message)
        self.menu_search_more.addSeparator()
        self.menu_search_more.addAction(self.menu_search_revision_range)
        self.menu_search_more.addAction(self.menu_search_revision)
        self.menu_search_more.addSeparator()
        self.menu_search_more.addAction(self.menu_search_diff)

        self.search_menu.addAction(self.menu_search_date_range)
        self.search_menu.addAction(self.menu_search_grep)
        self.search_menu.addAction(self.menu_search_more.menuAction())

        self.menu_branch_view.addAction(self.menu_browse_branch)
        self.menu_branch_view.addAction(self.menu_browse_other_branch)
        self.menu_branch_view.addSeparator()
        self.menu_branch_view.addAction(self.menu_visualize_current)
        self.menu_branch_view.addAction(self.menu_visualize_all)

        self.menu_branch_advanced.addAction(self.menu_diff_branch)

        self.branch_menu.addAction(self.menu_branch_review)
        self.branch_menu.addSeparator()
        self.branch_menu.addAction(self.menu_create_branch)
        self.branch_menu.addAction(self.menu_checkout_branch)
        self.branch_menu.addAction(self.menu_rebase_branch)
        self.branch_menu.addAction(self.menu_delete_branch)
        self.branch_menu.addSeparator()
        self.branch_menu.addAction(self.menu_branch_view.menuAction())
        self.branch_menu.addAction(self.menu_branch_advanced.menuAction())
        self.file_menu.addAction(self.menu_open_repo)
        self.file_menu.addAction(self.menu_clone_repo)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.menu_rescan)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.menu_manage_bookmarks)
        self.file_menu.addAction(self.menu_save_bookmark)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.menu_load_commitmsg)
        self.file_menu.addAction(self.menu_get_prev_commitmsg)
        self.file_menu.addAction(self.menu_load_commitmsg_template)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.menu_quit)
        self.merge_menu.addAction(self.menu_merge_local)
        self.merge_menu.addAction(self.menu_merge_abort)
        self.help_menu.addAction(self.menu_help_docs)
        self.help_menu.addAction(self.menu_help_about)
        self.diff_menu.addAction(self.menu_branch_diff)
        self.diff_menu.addAction(self.menu_diff_expression)
        self.diff_menu.addSeparator()
        self.diff_menu.addAction(self.menu_branch_compare)
        self.diff_menu.addAction(self.menu_commit_compare)
        self.diff_menu.addAction(self.menu_commit_compare_file)
        self.menu_tools.addAction(self.menu_tools_classic)
        self.menubar.addAction(self.file_menu.menuAction())
        self.menubar.addAction(self.edit_menu.menuAction())
        self.menubar.addAction(self.search_menu.menuAction())
        self.menubar.addAction(self.commit_menu.menuAction())
        self.menubar.addAction(self.branch_menu.menuAction())
        self.menubar.addAction(self.merge_menu.menuAction())
        self.menubar.addAction(self.diff_menu.menuAction())
        self.menubar.addAction(self.menu_tools.menuAction())
        self.menubar.addAction(self.help_menu.menuAction())

        top = QtCore.Qt.DockWidgetArea(4)
        bottom = QtCore.Qt.DockWidgetArea(8)

        self.addDockWidget(top, self.commitdockwidget)
        self.addDockWidget(top, self.statusdockwidget)
        self.addDockWidget(bottom, self.actiondockwidget)
        self.addDockWidget(bottom, self.logdockwidget)
        self.tabifyDockWidget(self.logdockwidget, self.diffdockwidget)
    
        # Translate
        self.status_tree.setAllColumnsShowFocus(True)
        self.status_tree.setSortingEnabled(False)
        self.status_tree.topLevelItem(0).setText(0, tr("Staged"))
        self.status_tree.topLevelItem(1).setText(0, tr("Modified"))
        self.status_tree.topLevelItem(2).setText(0, tr("Unmerged"))
        self.status_tree.topLevelItem(3).setText(0, tr("Untracked"))
        self.menu_show_diffstat.setShortcut(tr("Ctrl+D"))
        self.menu_stage_modified.setShortcut(tr("Alt+A"))
        self.menu_stage_untracked.setShortcut(tr("Alt+U"))
        self.menu_stage_selected.setShortcut(tr("Alt+T"))
        self.menu_export_patches.setShortcut(tr("Ctrl+E"))
        self.menu_cut.setShortcut(tr("Ctrl+X"))
        self.menu_copy.setShortcut(tr("Ctrl+C"))
        self.menu_paste.setShortcut(tr("Ctrl+V"))
        self.menu_select_all.setShortcut(tr("Ctrl+A"))
        self.menu_options.setShortcut(tr("Ctrl+O"))
        self.menu_delete.setShortcut(tr("Del"))
        self.menu_undo.setShortcut(tr("Ctrl+Z"))
        self.menu_redo.setShortcut(tr("Ctrl+Shift+Z"))
        self.menu_rescan.setShortcut(tr("Ctrl+R"))
        self.menu_cherry_pick.setShortcut(tr("Ctrl+P"))
        self.menu_quit.setShortcut(tr("Ctrl+Q"))
        self.menu_create_branch.setShortcut(tr("Ctrl+B"))
        self.menu_checkout_branch.setShortcut(tr("Alt+B"))
        self.menu_stash.setShortcut(tr("Alt+Shift+S"))
        self.menu_help_docs.setShortcut(tr("F1"))

    def create_dock(self, title):
        """Create a dock widget and set it up accordingly."""
        dock = QtGui.QDockWidget(self)
        dock.setWindowTitle(tr(title))
        dock.setObjectName(title)
        return dock

    def create_menu(self, title, parent):
        """Create a menu and set its title."""
        qmenu = QtGui.QMenu(parent)
        qmenu.setTitle(tr(title))
        return qmenu

    def create_action(self, title):
        """Create an action and set its title."""
        action = QtGui.QAction(self)
        action.setText(tr(title))
        return action

    def create_button(self, text, parent):
        """Create a button, set its title, and add it to the parent."""
        button = QtGui.QPushButton(parent)
        button.setText(tr(text))
        parent.layout().addWidget(button)
        return button