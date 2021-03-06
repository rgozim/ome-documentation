OMERO.server overview
=====================

OMERO sequence narrative
------------------------

Trying to understand all of what goes on with the server can be a bit
complicated. This short narrative tries to touch on the most critical
aspects.

-  A request reaches the server over
   one of the two remoting protocols: RMI or ICE. First, the
   :source:`Principal <components/common/src/ome/system/Principal.java>`
   is examined for a valid :doc:`session </developers/Server/Sessions>` which
   was created via :source:`ISession.createSession(String username, String
   password) <components/common/src/ome/api/ISession.java>`.

-  These values are checked against the ``experimenter``,
   ``experimentergroup`` and ``password`` tables. A valid login consists
   of a user name which is to be found in the ``omename`` column of
   ``experimenter``. This row from ``experimenter`` must also be
   contained in the "user" experimenter group which is done via the
   mapping table ``groupexperimentermap`` (see :source:`this SQL
   template <components/dsl/resources/ome/dsl/psql-footer.vm>`
   for how ``root`` and the intial groups are setup).

-  If the server is configured for :doc:`LDAP Authentication
   </sysadmins/server-ldap>`, an ``Experimenter`` may be
   created when ISessions attempts to check the password via
   ``IAdmin.checkPassword()``.

-  If authentication occurs, the request is passed to an
   `EJB3 <http://www.oracle.com/technetwork/java/javaee/ejb/index.html>`_ 
   interceptor which checks
   whether or not the authenticated user is authorized for that service
   method. Methods are labelled either ``@RolesAllowed("user")``,
   ``@RolesAllowed("system")``, or ``@PermitAll``. All users are a
   member of "user", but only administrators will be able to run
   "system" methods.

-  If authorization occurs, the request finally reaches a
   container-managed stateful or stateless 
   :doc:`service </developers/Modules/Api>` The
   service will :doc:`prepare </developers/Server/Aop>`
   the OMERO runtime for the
   particular user -- checking method parameters, creating a new 
   :doc:`event </developers/Server/Events>`, initializing the
   :doc:`security system </developers/Server/SecuritySystem>`, 
   etc. -- and pass execution onto the method implementation.
   This is done using references acquired (or injected) from the Spring
   :doc:`application context </developers/Server/Context>`.

-  The actual service implementation (from
   :sourcedir:`ome.logic <components/server/src/ome/logic>`
   or
   :sourcedir:`ome.services <components/server/src/ome/services>`)
   will be either read-only
   (:source:`IQuery <components/common/src/ome/api/IQuery.java>`-based)
   or a read-write
   (:source:`IUpdate <components/common/src/ome/api/IUpdate.java>`-based).

-  In the case of a read-only action, the implementation asks the
   database layer for the needed object graph, transforms them where
   necessary, and returns the values to the remoting subsystem. On the
   client-side, the returned graph can be mapped to an internal model
   via the ((OMERO Model Mapping\|model wrapper)).

-  In the case of a read-write action, the change to the database is
   first passed to a validation layer for extensive checking. Then the
   graph is passed to the database layer which prepares the SQL,
   including an audit trail of the changes made to the database.

-  After execution, the OMERO runtime is reset, the method call is
   logged, and either the successful results are returned or an
   :doc:`exception </developers/Modules/ExceptionHandling>` is thrown.

Technologies
------------

It is fairly easy to work with the server without understanding all of
its layers. The API is clearly outlined in the ome.api package and the
client proxies work almost as if the calls were being made from within
the same virtual machine. The only current caveat is that objects
returned between two different calls will not be referentially (i.e.
obj1 == obj2) equivalent. We are working on removing this restriction.

To understand the full technology stack, however, there are several
concepts which are of importance:

-  A layered architecture ensures that components only "talk to" the
   minimum necessary number of other components. This reduces the
   complexity of the entire system. Ensuring a loose-coupling of various
   components is facilitated by dependency injection. Dependency
   injection is the process of allowing a managing component to place a
   needed resource in a component's hand. Code for lookup or creation of
   resources, in turn, is unneeded, and explicit implementation details
   do not need to be hard-coded.

-  Object-relational mapping (ORM) is the process of mapping relational
   tables to object-oriented classes. Currently OMERO uses Hibernate_
   to provide this functionality. ORM allows the developer to work in a
   known environment, here the type-safe world of Java, rather than
   writing difficult to debug sql.

-  Aspect-oriented programming, a somewhat new and misunderstood
   technology, is perhaps the last technology which should be mentioned.
   Various pieces of code ("aspects") are *inserted* at various moments
   ("joinpoints") of execution. Collecting logic into aspects, whether
   logging, transactions, security etc., also reduces the overall
   complexity of the code.

Server design
-------------

.. figure:: /images/server-arch.png
   :align: center
   :alt: Server Architecture

   Server Architecture

.. figure:: /images/server-design.png
   :align: center
   :alt: Server Design

   Server Design

The server logic resides in the :sourcedir:`components/server`
component.

Topics
~~~~~~

-  :doc:`/developers/Modules/ExceptionHandling`
-  |OmeroModel|
-  :doc:`/sysadmins/server-security`


.. seealso:: |OmeroGrid|
